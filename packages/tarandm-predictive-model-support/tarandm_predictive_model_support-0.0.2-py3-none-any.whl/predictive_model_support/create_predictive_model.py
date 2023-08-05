import datetime

import structlog

import base64
import io
import pickle
import zipfile
from typing import List, Dict, Union, Optional, Any, Tuple

from aiohttp import ClientTimeout, ClientSession
from path import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import Booster
from sklearn.metrics import roc_auc_score
import os

import pandas as pd

from predictive_model_support.model_vizualization import (
    shap_summary_plot_logistic_regression,
    shap_summary_plot_xgboost,
    shap_summary_plot_random_forest,
    learning_curves_plot,
)

logger = structlog.get_logger(__name__)


def evaluate_auc(label, prediction) -> float:
    if len(set(label)) == 1:
        raise ValueError("Only one class present in y_true. ROC AUC score is not defined in that case.")
    elif len(set(label)) > 2:
        raise ValueError(
            f"AUC evaluation supports only binary labels. Provided label contains {len(set(label))} unique " f"values"
        )

    return roc_auc_score(y_true=label, y_score=prediction)


def evaluate_gini(label, prediction) -> float:
    return 2 * evaluate_auc(label, prediction) - 1


def get_predictive_model_performance(
    data: pd.DataFrame,
    column_name_sample: Optional[str],
    column_name_prediction: str,
    evaluate_performance: Dict[str, Union[str, List[str]]],
) -> Optional[List[Dict[str, Any]]]:
    """
    Function calculates different performance metrics of predictive model.

    :param data: Dataset to be used for evaluating performance.
    :param column_name_sample: Name of the column inside 'data' that distinguishes type of data samples. Column can
           contain for instance values 'train', 'valid', 'test'. This will define which observations belong to train
           set, validation set and test set.
    :param column_name_prediction: Name of the column inside 'data' that holds values of predictive model prediction.
    :param evaluate_performance: Dictionary that defines what metrics should be evaluated. Keys in dictionary must refer
           to columns in 'data' that will be used as true label. Multiple true label columns can be defined. This can be
           useful for instance in situations when we have binary labels (indicators of an event) calculated over
           different time windows. In values under each key, metrics to be evaluated are defined.

           Example:
           evaluate_performance = {
               'label_3M': 'AUC',
               'label_12M': ['AUC', 'GINI']
           }
    :return: Dictionary with calculated performance metrics.
    """

    if column_name_sample is None:
        logger.warning(
            "Evaluating model performance: Column name with sample type was not provided. All observations will be treated as training data."
        )
        column_name_sample = _generate_sample_type_column_name(data=data)
        data[column_name_sample] = "train"
    elif column_name_sample not in data.columns:
        logger.warning(
            f"Evaluating model performance: Provided column name with sample type '{column_name_sample}' does not exist in data. All observations will be treated as training data."
        )
        column_name_sample = _generate_sample_type_column_name(data=data)
        data[column_name_sample] = "train"

    implemented_performance_metrics = {"AUC": evaluate_auc, "GINI": evaluate_gini}

    performance = []
    included_sample_types = data[column_name_sample].unique()
    for label, metrics in evaluate_performance.items():
        if isinstance(metrics, str):
            metrics = [metrics]

        for sample in included_sample_types:
            mask = data[column_name_sample] == sample
            performance_by_metric = {}
            for metric in metrics:
                if metric.upper() not in implemented_performance_metrics:
                    logger.warning(
                        f"Requested metric '{metric}' is not supported. Value for '{metric}' will not be stored. Supported performance metrices are: {', '.join(implemented_performance_metrics)}"
                    )
                else:
                    metric_value = implemented_performance_metrics[metric.upper()](
                        data[mask][label], data[mask][column_name_prediction]
                    )
                    performance_by_metric[metric.upper()] = metric_value

            performance.append({"target": label, "sample": sample.upper(), "performance": performance_by_metric})

    return performance


def _generate_sample_type_column_name(data: pd.DataFrame) -> str:
    if "sample" not in data.columns:
        return "sample"
    else:
        for i in range(1, 10000):
            if f"sample_{i}" not in data.columns:
                return f"sample_{i}"
    return "column_with_sample_type"


def _get_data_sample_description(
    data: pd.DataFrame,
    column_name_label: Optional[str] = None,
    column_name_sample: Optional[str] = None,
    column_name_date: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Function evaluates different descriptive information about model development data sample, such as what time range
    was used, what are the frequencies of label classes and other.

    :param data: Dataset to be used for descriptive info evaluation.
    :param column_name_label: Name of the column inside 'data' that stores labels.
    :param column_name_sample: Name of the column inside 'data' that distinguishes type of data samples. Column can
           contain for instance values 'train', 'valid', 'test'. This will define which observations belong to train
           set, validation set and test set.
    :param column_name_date: Name of the column inside 'data' that stores dates related to observations.
    :return: Dictionary with descriptive info data.
    """
    if column_name_sample is None:
        logger.warning(
            "Preparing sample descriptions: Column name with sample type was not provided. All observations will be treated as training data."
        )
        column_name_sample = _generate_sample_type_column_name(data=data)
        data[column_name_sample] = "train"
    elif column_name_sample not in data.columns:
        logger.warning(
            f"Preparing sample descriptions: Provided column name with sample type '{column_name_sample}' does not exist in data. All observations will be treated as training data."
        )
        column_name_sample = _generate_sample_type_column_name(data=data)
        data[column_name_sample] = "train"

    date_available = True
    if column_name_date is None:
        logger.warning(
            "Date column name (column_name_date) was not provided. Time related metadata will not be evaluated."
        )
        date_available = False
    elif column_name_date not in data.columns:
        logger.warning(
            f"Provided date column name '{column_name_date}' does not exist in data. Time related metadata will not be evaluated."
        )
        date_available = False
    elif data[column_name_date].dtype != "<M8[ns]":
        print(
            f"Provided date column name '{column_name_date}' is of type {data[column_name_date].dtype.__str__()}. Required type is '<M8[ns]. Time related metadata will not be evaluated."
        )
        date_available = False

    label_available = True
    label_binary = True
    if column_name_label is None:
        logger.warning(f"Label column name was not provided. Label related metadata will not be evaluated.")
        label_available = False
    elif column_name_label not in data.columns:
        logger.warning(
            f"Provided label column name '{column_name_label}' does not exist in data. Label related metadata will not be evaluated."
        )
        label_available = False
    elif data[column_name_label].nunique() != 2:
        label_binary = False

    included_sample_types = data[column_name_sample].unique()

    result = []
    for sample_type in included_sample_types:
        sample_meta = {"sample_type": sample_type.upper()}
        mask = data[column_name_sample] == sample_type
        sample_meta["number_of_observations"] = len(data[mask])

        if date_available:
            sample_meta["first_date"] = data[mask][column_name_date].min().strftime(format="%Y-%m-%d")
            sample_meta["last_date"] = data[mask][column_name_date].max().strftime(format="%Y-%m-%d")

        if label_available and label_binary:
            sample_meta["label_class_frequency"] = []
            for label_class in data[column_name_label].unique().tolist():
                sample_meta["label_class_frequency"].append(
                    {
                        "label_class": label_class,
                        "number_of_observations": len(data[mask & (data[column_name_label] == label_class)]),
                    }
                )
        result.append(sample_meta)

    return result


def _get_model_type(model: Any, supported_model_types: List[str]) -> str:

    if isinstance(model, LogisticRegression):
        logger.info("Automatically assigned model type LOGISTIC_REGRESSION.")
        return "LOGISTIC_REGRESSION"
    elif isinstance(model, RandomForestClassifier):
        logger.info("Automatically added model type RANDOM_FOREST.")
        return "RANDOM_FOREST"
    elif isinstance(model, Booster):
        logger.info("Automatically added model type XGB.")
        return "XGB"
    elif isinstance(model, pd.DataFrame):
        logger.info("Automatically added model type EXPERT_SCORE.")
        return "EXPERT_SCORE"
    else:
        raise TypeError(
            f"Model type was not provided and neither detected automatically. Available model types are: {supported_model_types}"
        )


def _generate_model_name(model_type: str) -> str:
    return f"{model_type.lower()}_{datetime.datetime.now().strftime(format='%Y%m%d%H%M%S')}"


def _generate_images(
    data: pd.DataFrame,
    attributes: List[str],
    model: Any,
    model_type: str,
    target_class: Optional[str] = None,
    learning_curves_data: Optional[Dict] = None,
) -> Tuple[List[Dict], List[Dict]]:
    images = []
    images_meta = []
    if model_type == "LOGISTIC_REGRESSION":
        try:
            img = shap_summary_plot_logistic_regression(model=model, data=data, attributes=attributes)
            images_meta.append({"filename": "shap_summary.svg", "type": "shap_summary"})
            images.append({"filename": "shap_summary.svg", "image": img})
        except Exception as e:
            logger.warning(f"Failed to generate Shap summary plot: {e}")
    elif model_type == "XGB":
        img = shap_summary_plot_xgboost(model=model, data=data, attributes=attributes)
        images_meta.append({"filename": "shap_summary.svg", "type": "shap_summary"})
        images.append({"filename": "shap_summary.svg", "image": img})

        if learning_curves_data is not None and len(learning_curves_data) > 0:
            img = learning_curves_plot(model=model, evaluations_result=learning_curves_data, metric=None)
            images_meta.append({"filename": "learning_curves.svg", "type": "learning_curves"})
            images.append({"filename": "learning_curves.svg", "image": img})
    elif model_type == "RANDOM_FOREST":
        img = shap_summary_plot_random_forest(model=model, data=data, attributes=attributes, target_class=target_class)
        images_meta.append({"filename": "shap_summary.svg", "type": "shap_summary"})
        images.append({"filename": "shap_summary.svg", "image": img})

    return images, images_meta


def prepare_predictive_model_data(
    model: Union[LogisticRegression, RandomForestClassifier, Booster, pd.DataFrame],
    attributes: List[str],
    model_name: Optional[str] = None,
    model_type: Optional[str] = None,
    data: Optional[pd.DataFrame] = None,
    label_name: Optional[str] = None,
    target_class: Optional[str] = None,
    attribute_binning: Optional[Dict] = None,
    attribute_transformation: Optional[Dict[str, str]] = None,
    hyperparameters: Optional[Dict] = None,
    general_notes: Optional[Union[Dict, List[str], str]] = {},
    attribute_description: Optional[Dict[str, str]] = None,
    column_name_sample: Optional[str] = None,
    column_name_date: Optional[str] = None,
    column_name_prediction: Optional[str] = None,
    evaluate_performance: Optional[Dict[str, Union[str, List[str]]]] = None,
    learning_curves_data: Optional[Dict] = None,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Function prepares input data for build model zip file, that is ready to be implemented in TaranDM software.
    Created input data will be sent to the TaranDM endpoint, through which final model zip file is returned.

    :param model: Trained predictive model. One of from "sklearn.ensemble.RandomForestClassifier",
    "sklearn.linear_model.LogisticRegression", "xgboost.Booster", "pd.DataFrame". "pd.DataFrame" represents expert
    scorecard model, where user manually defines values for predictor bins.
    :param attributes: List of model predictors.
    :param model_name: Name of the model (will be visible in TaranDM GUI).
    :param model_type: Type of the model. One of "XGB", "LOGISTIC_REGRESSION", "RANDOM_FOREST", "EXPERT_SCORE".
    :param data: Dataset used for model training. Required to calculate model performance, and descriptive statistics
    about development sample.
    :param label_name: Name of the target variable. Should be included in data to properly evaluate model performance.
    :param target_class: Target class predicted by the model.
    :param attribute_binning: Attribute binning (if applied). In inference phase, we first apply predictor
    transformation (if defined) and then binning. Resulting value is passed to model predict method.

    Binning should be provided as a dictionary with following structure:
    binning = {
        'numerical_predictor1': {
            'dtype': 'NUMERICAL',
            'bins': [-np.inf, 20, 35, 50, np.inf],
            'bin_vals': [1, 2, 3, 4, 1000],
            'null_val': 0
        },
        'categorical_predictor1': {
            'dtype': 'CATEGORICAL',
            'bins': [['M'], ['F']]',
            'bin_vals': [1, 2, 3, 4, 1000],
            'null_val': 0
        },
        ...
    }
    Keys of provided dictionary are names of the predictors. TaranDM supports 'NUMERICAL' and 'CATEGORICAL' data
    types of predictors. For numerical predictors, binning is defined by providing list of bin borders. For
    categorical predictors, binning is defined by providing list of lists. Inner lists define values that belong
    to each group. Both 'NUMERICAL' and 'CATEGORICAL' data types contain attributes 'bin_vals' and
    'null_val'. Those are values used for encoding the bins. 'null_val' is an encoding value for null values
    (missings).

    :param attribute_transformation: Transformation of the predictors. Transformation is applied before binning. If both
    transformation and binning are defined, predictor is first transformed and binning is applied over values
    obtained after transformation.

    Transformation should be provided as a dictionary with following structure:
    transformation = {
        'numerical_predictor1': '{numerical_predictor1} + 1'
        ...
    }
    In transformation formula, anything in "{}" is considered as predictor and will be replaced with predictor value
    during formula evaluation.

    :param hyperparameters: Model hyperparameters.
    :param general_notes: Dictionary of general notes about the model. Notes will be displayed in GUI.
    :param attribute_description: Dictionary with description of predictors.
    :param column_name_sample: Name of the column in data, that defines different data sample types (train, test, etc.).
    If provided, sample statistics will be stored in model metadata.
    :param column_name_date: Name of the column in data, that defines time dimension. If provided, information about
    time range used in development sample data will be stored in model metadata.
    :param column_name_prediction: Name of the column in data, that holds model prediction. This column is used to
    evaluate model performance.
    :param evaluate_performance: Dictionary that defines performance to be evaluated - which target and over which
    sample types. Use following structure:

    evaluate_performance = {
    }
    :param learning_curves_data: Data for plotting learning curves plot in following structure:

    learning_curves_data = {
        'sample1': {
            'metric1': [
                0.5,
                0.4,
                0.3
            ]
        },
        'sample2': {
            'metric1': [
                0.6,
                0.5,
                0.4
            ]
        }
    }
    :return:
    """

    supported_model_types = ["XGB", "LOGISTIC_REGRESSION", "RANDOM_FOREST", "EXPERT_SCORE"]

    if model_type is None:
        model_type_final = _get_model_type(model=model, supported_model_types=supported_model_types)
    elif model_type not in supported_model_types:
        logger.warning(
            f"Model type '{model_type}' is invalid. Supported model types are: {', '.join(supported_model_types)}. "
            f"Will try to detect model type automatically."
        )
        model_type_final = _get_model_type(model=model, supported_model_types=supported_model_types)
    else:
        model_type_final = model_type

    if model_name is None:
        model_name_final = _generate_model_name(model_type=model_type_final)
        logger.warning(f"Model name was not provided. Generated model name: '{model_name_final}'.")
    else:
        model_name_final = model_name

    model_binary = pickle.dumps(model)
    model_binary_encoded = base64.b64encode(model_binary)
    model_binary_encoded_string = model_binary_encoded.decode("ascii")
    request_data = {
        "model": model_binary_encoded_string,
        "predictors": attributes,
        "model_name": model_name_final,
        "model_type": model_type_final,
    }

    if data is None:
        logger.warning("No dataset was provided. Cannot evaluate sample description data.")
    elif len(data) == 0:
        logger.warning("Provided dataset has 0 observations. Cannot evaluate sample description data.")
    else:
        request_data["sample_description_data"] = _get_data_sample_description(
            data=data,
            column_name_label=label_name,
            column_name_sample=column_name_sample,
            column_name_date=column_name_date,
        )

    if general_notes:
        request_data["general_notes"] = general_notes
    if hyperparameters:
        request_data["hyperparameters"] = hyperparameters
    if label_name:
        request_data["label_name"] = label_name
    if target_class:
        request_data["target_class"] = target_class
    if attribute_binning:
        request_data["attribute_binning"] = attribute_binning
    if attribute_transformation:
        request_data["attribute_transformation"] = attribute_transformation
    if attribute_description:
        request_data["attribute_description"] = attribute_description

    if evaluate_performance is not None:
        if data is None:
            logger.warning("No dataset was provided. Cannot evaluate model performance.")
        elif len(data) == 0:
            logger.warning("Provided dataset has 0 observations. Cannot evaluate model performance.")
        elif column_name_prediction is None:
            logger.warning(
                "Name of the columns that holds predictions (column_name_prediction) was not provided. Cannot evaluate model performance."
            )
        elif column_name_prediction not in data.columns:
            logger.warning(
                f"Provided name of the columns that holds predictions '{column_name_prediction}' is not in data. Cannot evaluate model performance."
            )
        else:
            request_data["model_performance"] = get_predictive_model_performance(
                data=data,
                column_name_sample=column_name_sample,
                column_name_prediction=column_name_prediction,
                evaluate_performance=evaluate_performance,
            )

    images, images_meta = _generate_images(
        data=data,
        attributes=attributes,
        model=model,
        model_type=model_type_final,
        target_class=target_class,
        learning_curves_data=learning_curves_data,
    )
    request_data["attached_images"] = images_meta

    return request_data, images


async def build_predictive_model(
    request_data,
    images: List[Dict[str, Any]],
    filename: str,
    url: str = "https://dm.develop.demo.tarandm.com/api/doc",
) -> None:
    url += "/analytics/build_predictive_model"
    async with ClientSession(timeout=ClientTimeout(total=30)) as session:
        response = await session.get(url=url, json=request_data)
        response_data = await response.json()

        if response.status == 500:
            # TODO raise proper error type
            raise ValueError(f"{response_data['message']}")
        extended_model_yaml = response_data["extended_predictive_model_yaml"]
        external_model_json = response_data["external_model_json"]

        save_to_zip(extended_model_yaml, external_model_json, images, filename)


def save_to_zip(
    extended_model_yaml: str, external_model_json: str, images: List[Dict[str, Any]], filename: str
) -> None:
    def add_file(archive, buffer, name):
        if isinstance(buffer, io.StringIO):
            buffer.seek(0)
            buffer = io.BytesIO(buffer.read().encode())
        buffer.seek(0, os.SEEK_END)
        buffer.seek(0)
        archive.writestr(name, buffer.getvalue())

    out = io.BytesIO()
    with zipfile.ZipFile(file=out, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        add_file(zf, io.StringIO(extended_model_yaml), "extended_model.yaml")
        add_file(zf, io.StringIO(external_model_json), "external_model.json")
        for img in images:
            add_file(zf, img["image"], img["filename"])

    path = Path(filename)
    if not path.endswith(".zip"):
        path += ".zip"

    with open(path, "wb") as f:
        f.write(out.getbuffer())
