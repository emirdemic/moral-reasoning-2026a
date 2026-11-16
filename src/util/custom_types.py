import typing as t


class NormalityTestResult(t.TypedDict):
    w: float
    p_value: float
    normal: bool


class ContinuousVariableDescriptive(t.TypedDict):
    median: float
    mean: float
    std: float
    sk: float
    ku: float
    min_value: float
    max_value: float
    missing: int
    normality: NormalityTestResult | None
    sample_size: int


class CronbachAlpha(t.TypedDict):
    alpha: float
    lower_bound: float
    upper_bound: float


class CorrelationValue(t.TypedDict):
    r: float
    lower_bound: float
    upper_bound: float
    p_value: float


class SubscaleDescriptive(ContinuousVariableDescriptive):
    cronbach_alpha: CronbachAlpha


class ItemDescriptive(ContinuousVariableDescriptive):
    corrected_item_total_r: CorrelationValue


class CategoricalVariableDescriptive(t.TypedDict):
    proportions: dict[str | int, float]
    counts: dict[str | int, float]
    missing: int
    sample_size: int
