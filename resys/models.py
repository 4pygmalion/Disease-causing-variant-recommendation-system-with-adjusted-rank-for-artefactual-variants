import os
import sys
import pickle
import numpy as np
from typing import Dict, AnyStr
from logging import Logger


def convert_ad_to_vaf(ad: str) -> float:
    """AD값을 VAF값으로 변환
    Args:
        ad: allele depth
    Return:
        vcf (int): variant allele fraction (=variant AD / DP)
    """

    try:
        ref, *alt = map(int, str(ad).split(","))
    except:
        return 0

    n_alt = sum(alt)
    n_total = n_alt + ref
    return n_alt / (n_total) if n_total != 0 else 0

class Classifier:
    def __init__(
        self,
        config: dict,
        logger: Logger = Logger(name="classifier"),
    ):
        self.config = config
        self.logger = logger

    def set_model(self):
        model_path = self.config["MODEL"]["PATH"]
        if not os.path.exists(model_path):
            FileNotFoundError(f"model_path ({model_path}) not found")

        # TODO: ONNX runtime로 서빙
        with open(model_path, "rb") as fh:
            self.model = pickle.load(fh)

        return

    def featurize(self, feature_info: dict, inhouse_total_ac: int) -> None:
        """gene_diseases 내에 변이별 QUAL, AD을 이용해 특징값을 생성

        Args:
            feature_info (dict): variant의 특징값
            inhouse_samples (int): 전체 샘플에서의 ac

        Example:
            >>> feature_info = {
                "acmg_bayesian": "0.89",
                "ad": "238,27",
                "qual": "121.73",
                "disease_similarity": "3.523",
                "inhouse_variant_ac": "441",
            }
            >>> self.featurize(feature_info, inhouse_total_ac=45000)
        """
        feature_info["vaf"] = convert_ad_to_vaf(feature_info["ad"])
        feature_info["inhouse_af"] = int(
            feature_info["inhouse_variant_ac"]
        ) / inhouse_total_ac

        return

    def make_batch(
        self, featured_gene_diseases: dict, inhouse_total_ac: int
    ) -> np.ndarray:

        batch = list()
        for gene_disease, varaint_info in featured_gene_diseases.items():
            for variant, feature_info in varaint_info.items():
                self.featurize(feature_info, inhouse_total_ac)
                batch.append(
                    [
                        float(feature_info[feature_name])
                        for feature_name in self.config["MODEL"][
                            "FEATURE_NAMES"
                        ]
                    ]
                )

        return np.array(batch)

    def post_process(self, gene_diseases: dict, y_hat: np.ndarray) -> dict:
        """예측값(y_hat)에 대해서 gene_disease 및 variant단위로 확률 값을 반환

        Args:
            gene_diseases (dict): gene_disease 및 variant정보
            y_hat (np.ndarray): 1차원 array
        """
        if y_hat.ndim != 1:
            raise ValueError(f"Expected 1D y_hat array, passed: {y_hat.ndim}")

        return_dict = dict()

        idx = 0
        for gene_disease, variant_info in gene_diseases.items():
            if gene_disease not in return_dict:
                return_dict[gene_disease] = dict()

            for variant, info in variant_info.items():
                return_dict[gene_disease][variant] = round(y_hat[idx], 5)
                idx += 1

        if idx != len(y_hat):
            self.logger.warning(
                f"Length of y_hat is not same with number of variant"
            )

        return return_dict

    def predict(self, query: dict) -> dict:
        """주어진 query에 따라 response해줌
        
        """
        self.logger.debug("In processing: make_batch")
        batches = self.make_batch(query["gene_diseases"], query["inhouse_total_ac"])

        self.logger.debug("In processing: predict proba")
        y_hat = self.model.predict_proba(batches)[:, 1]

        self.logger.debug("In processing: post process")
        return self.post_process(query["gene_diseases"], y_hat)
