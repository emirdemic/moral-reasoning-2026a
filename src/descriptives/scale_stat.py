from pandera.typing import DataFrame
import numpy as np
import pingouin as pn
from dataclasses import dataclass
import yaml

from src.util.custom_types import ItemDescriptive, SubscaleDescriptive, CronbachAlpha, CorrelationValue
from src.descriptives.descriptive_stat import get_continuous_variable_descriptive


@dataclass
class ScaleStat:
    items: DataFrame
    subscales: DataFrame
    item_subscale_map: dict[str, list[str]]

    @classmethod
    def from_survey_description(cls, dataframe: DataFrame, survey: str):
        with open("data/survey_descriptions.yaml", "r", encoding="utf-8") as file:
            survey_desc = yaml.safe_load(file)[survey]
        items = [i["name"] for s in survey_desc["subscales"] for i in s["items"]]
        subscale_map = {
            s["name"]: [i["name"] for i in s["items"]] for s in survey_desc["subscales"]
        }
        return cls(
            items=dataframe[items],
            subscales=dataframe[[s["name"] for s in survey_desc["subscales"]]],
            item_subscale_map=subscale_map,
        )

    @staticmethod
    def recode_items(dataframe: DataFrame, survey: str) -> DataFrame:
        with open("data/survey_descriptions.yaml", "r", encoding="utf-8") as file:
            survey_desc = yaml.safe_load(file)[survey]
        to_recode = [
            i["name"]
            for s in survey_desc["subscales"]
            for i in s["items"]
            if i.get("reverse", False) is True
        ]
        maximum = survey_desc["maximum"]
        df_copy = dataframe.copy()
        for i in to_recode:
            df_copy[i] = df_copy[i].apply(lambda x: maximum + 1 - x)
        return df_copy

    def get_item_descriptives(self) -> dict[str, ItemDescriptive]:
        item_descriptives = {
            i: get_continuous_variable_descriptive(self.items, i) for i in self.items
        }
        for col in self.items:
            mean = self.items[[i for i in self.items if i != col]].mean(axis=1)
            corr = pn.corr(self.items[col], mean)
            item_descriptives[col]["corrected_item_total_r"] = CorrelationValue(
                r=round(corr.at["pearson", "r"], 2),
                p_value=round(corr.at["pearson", "p-val"], 5),
                lower_bound=round(corr.at["pearson", "CI95%"][0], 2),
                upper_bound=round(corr.at["pearson", "CI95%"][1], 2),
            )
        return {i: ItemDescriptive(**j) for i, j in item_descriptives.items()}

    def get_mean_corrected_item_total_r(self) -> float:
        item_descriptives = self.get_item_descriptives()
        correlations = [r["corrected_item_total_r"]["r"] for _, r in item_descriptives.items()]
        return np.nanmean(correlations)

    def get_subscale_descriptives(self) -> dict[str, SubscaleDescriptive]:
        scale_descriptives = {
            i: get_continuous_variable_descriptive(self.subscales, i) for i in self.subscales
        }
        for s in self.subscales:
            items = self.items[self.item_subscale_map[s]]
            alpha = pn.cronbach_alpha(items)
            scale_descriptives[s].update(
                {
                    "cronbach_alpha": CronbachAlpha(
                        alpha=alpha[0],
                        lower_bound=alpha[1][0],
                        upper_bound=alpha[1][1],
                    ),
                }
            )
        return {i: SubscaleDescriptive(**j) for i, j in scale_descriptives.items()}

    def get_subscale_pairwise_corr(self) -> DataFrame | None:
        if self.subscales.shape[1] <= 1:
            return
        return pn.pairwise_corr(self.subscales, padjust="bonf")

    def get_scale_reliability(self) -> CronbachAlpha:
        alpha = pn.cronbach_alpha(self.items)
        return CronbachAlpha(
            alpha=alpha[0], lower_bound=alpha[1][0], upper_bound=alpha[1][1]
        )
