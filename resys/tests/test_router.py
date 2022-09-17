import os
import sys
import pytest

TEST_DIR = os.path.dirname(__file__)
ASC3_DIR = os.path.dirname(TEST_DIR)
sys.path.append(ASC3_DIR)

from routers import check_query


@pytest.mark.parametrize(
    "query, expected",
    [
        pytest.param(
            {"inhouse_total_ac": 100, "gene_diseases": {}},
            {
                "status": "error",
                "data": dict(),
                "message": "sample_id not passed",
            },
            id="TEST1: not found sample_id",
        ),
        pytest.param(
            {
                "sample_id": "TEST_ID",
                "inhouse_total_ac": 100,
                "gene_diseases": {},
            },
            dict(),
            id="TEST2: success",
        ),
        pytest.param(
            {
                "sample_id": "TEST_ID",
                "gene_diseases": {},
            },
            {
                "status": "error",
                "data": dict(),
                "message": "inhouse_total_ac not passed",
            },
            id="TEST3: not found inhouse_total ac",
        ),
        pytest.param(
            {
                "sample_id": "TEST_ID",
            },
            {
                "status": "error",
                "data": dict(),
                "message": "gene_diseases, inhouse_total_ac not passed",
            },
            id="TEST4: not found inhouse total ac, gene disease",
        ),
        pytest.param(
            {
                "sample_id": "test_id",
                "inhouse_total_ac": 100,
                "gene_diseases": {
                    "OMIM:600276-OMIM:125310": {
                        "1-100-A-T": {
                            "acmg_bayesian": 1,
                            "qual": 1271.77,
                            "ad": "287.27",
                            "dp": 129.0,
                            "disease_similarity": 3.09534946,
                            "inhouse_variant_ac": 237,
                        },
                        "1-200-A-T": {
                            "acmg_bayesian": 0.99409,
                            "qual": 1271.77,
                            "ad": "287.27",
                            "dp": 129.0,
                            "disease_similarity": 5.09534946,
                            "inhouse_variant_ac": 3,
                        },
                    },
                    "OMIM:12367-OMIM:23223": {
                        "3-100-A-T": {
                            "acmg_bayesian": 0.99409,
                            "qual": 1271.77,
                            "ad": "287.27",
                            "dp": 129.0,
                            "disease_similarity": -1.09534946,
                            "inhouse_variant_ac": 237,
                        },
                        "3-200-A-T": {
                            "acmg_bayesian": 0.99409,
                            "qual": 1271.77,
                            "ad": "287.27",
                            "dp": 129.0,
                            "disease_similarity": -1.09534946,
                            "inhouse_variant_ac": 237,
                        },
                    },
                },
            },
            dict(),
            id="TEST5: success",
        ),
    ],
)
def test_check_query(query, expected):
    assert expected == check_query(query)
