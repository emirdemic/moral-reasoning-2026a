import numpy as np
from pandera.typing import DataFrame
import pingouin as pn
from scipy.stats import skew, kurtosis

from src.util.custom_types import (
    ContinuousVariableDescriptive,
    CategoricalVariableDescriptive,
    CorrelationValue,
    NormalityTestResult,
)


def get_continuous_variable_descriptive(dataframe: DataFrame, variable_name: str):
    normality = pn.normality(dataframe[variable_name])
    return ContinuousVariableDescriptive(
        median=round(np.nanmedian(dataframe[variable_name]), 2),
        mean=round(np.nanmean(dataframe[variable_name]), 2),
        std=round(np.nanstd(dataframe[variable_name], ddof=1), 2),
        sk=round(skew(dataframe[variable_name], nan_policy="omit"), 2),
        ku=round(kurtosis(dataframe[variable_name], nan_policy="omit", bias=False), 2),
        min_value=np.nanmin(dataframe[variable_name]),
        max_value=np.nanmax(dataframe[variable_name]),
        missing=int(dataframe[variable_name].isna().sum()),
        normality=NormalityTestResult(
            w=round(normality.at[variable_name, "W"], 2),
            p_value=round(normality.at[variable_name, "pval"], 5),
            normal=normality.at[variable_name, "normal"],
        ),
        sample_size=int(dataframe[variable_name].notna().sum()),
    )


def get_categorical_variable_descriptive(
    dataframe: DataFrame, variable_name: str, value_labels: dict | None = None
):
    value_labels = {} if value_labels is None else value_labels
    descriptive = dataframe[variable_name].agg(
        {
            "proportion": lambda a: round(a.value_counts(normalize=True) * 100, 2),
            "counts": lambda a: a.value_counts()
        }
    )
    descriptive.rename(
        index={i: value_labels.get(i, i) for _, i in descriptive.index}, inplace=True
    )
    return CategoricalVariableDescriptive(
        proportions=descriptive["proportion"].to_dict(),
        counts=descriptive["counts"].to_dict(),
        missing=int(dataframe[variable_name].isna().sum()),
        sample_size=int(dataframe[variable_name].notna().sum()),
    )


def get_correlation(variable_1, variable_2) -> dict[str, CorrelationValue]:
    corr_r = pn.corr(variable_1, variable_2)
    corr_s = pn.corr(variable_1, variable_2, method="spearman")
    return {
        "pearson": CorrelationValue(
            r=round(corr_r.at["pearson", "r"], 2),
            p_value=round(corr_r.at["pearson", "p-val"], 5),
            lower_bound=round(corr_r.at["pearson", "CI95%"][0], 2),
            upper_bound=round(corr_r.at["pearson", "CI95%"][1], 2),
        ),
        "spearman": CorrelationValue(
            r=round(corr_s.at["spearman", "r"], 2),
            p_value=round(corr_s.at["spearman", "p-val"], 5),
            lower_bound=round(corr_s.at["spearman", "CI95%"][0], 2),
            upper_bound=round(corr_s.at["spearman", "CI95%"][1], 2),
        ),
    }
