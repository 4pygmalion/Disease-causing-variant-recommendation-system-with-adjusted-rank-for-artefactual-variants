import os
import sys
import pytest
from unittest.mock import patch, Mock
import numpy as np

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ASC3_DIR = os.path.dirname(TESTS_DIR)
ROOT_DIR = os.path.dirname(ASC3_DIR)
sys.path.append(ASC3_DIR)

from models import Classifier
from utils import load_yaml


@pytest.fixture()
def config():
    return load_yaml(os.path.join(ASC3_DIR, "config.yaml"))


@pytest.fixture()
def classifier(config):
    return Classifier(config["API"], Mock())


def test_featurize(classifier):
    inhouse_total_ac = 45496
    feature_info = {
        "acmg_bayesian": "0.89",
        "ad": "238,27",
        "qual": "121.73",
        "disease_similarity": "3.523",
        "inhouse_variant_ac": "441",
    }
    classifier.featurize(feature_info, inhouse_total_ac)

    added_features = ["vaf", "inhouse_af"]

    assert all(
        added_feature in feature_info for added_feature in added_features
    )
    assert all(
        isinstance(feature_info[added_feature], float)
        for added_feature in added_features
    )


def test_make_batch(classifier):
    inhouse_total_ac = 45496
    featured_gene_diseases = {
        "OMIM:600276-OMIM:125310": {
            "19-15191971-G-A": {
                "acmg_bayesian": "0.89",
                "ad": "238,27",
                "qual": "121.73",
                "disease_similarity": "3.523",
                "inhouse_variant_ac": "441",
                "vaf": 0.1018867924528302,
                "inhouse_samples_ratio": 0.004846579919113768,
            },
            "19-15191971-GT-A": {
                "acmg_bayesian": "0.89",
                "ad": "238,27,2",
                "qual": "121.73",
                "disease_similarity": "3.523",
                "inhouse_variant_ac": "441",
                "vaf": 0.10861423220973783,
                "inhouse_samples_ratio": 0.004846579919113768,
            },
        },
        "OMIM:600276-OMIM:130720": {
            "19-15191999-G-A": {
                "acmg_bayesian": "0.89",
                "ad": "238,27",
                "qual": "121.73",
                "disease_similarity": "3.523",
                "inhouse_variant_ac": "441",
                "vaf": 0.1018867924528302,
                "inhouse_samples_ratio": 0.004846579919113768,
            }
        },
    }
    x = classifier.make_batch(featured_gene_diseases, inhouse_total_ac)

    assert isinstance(x, np.ndarray)
    assert x.dtype == "float64"


def test_post_process(classifier):
    y_hat = np.array([0, 0.5, 0.9])
    gene_diseases = {
        "OMIM:600276-OMIM:125310": {
            "19-15191971-G-A": {
                "acmg_bayesian": "0.89",
                "ad": "238,27",
                "qual": "121.73",
                "disease_similarity": "3.523",
                "inhouse_variant_ac": "441",
            },
            "19-15191971-GT-A": {
                "acmg_bayesian": "0.89",
                "ad": "238,27,2",
                "qual": "121.73",
                "disease_similarity": "3.523",
                "inhouse_variant_ac": "441",
            },
        },
        "OMIM:600276-OMIM:130720": {
            "19-15191999-G-A": {
                "acmg_bayesian": "0.89",
                "ad": "238,27",
                "qual": "121.73",
                "disease_similarity": "3.523",
                "inhouse_variant_ac": "441",
            }
        },
    }

    expected = {
        "OMIM:600276-OMIM:125310": {
            "19-15191971-G-A": 0.0,
            "19-15191971-GT-A": 0.5,
        },
        "OMIM:600276-OMIM:130720": {
            "19-15191999-G-A": 0.9,
        },
    }

    assert expected == classifier.post_process(gene_diseases, y_hat)
