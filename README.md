# Disease-causing variant recommendation system for Rare diseases 

: API containing a disease-causing variant recommendation system that integrates quality control into variant prioritization by adjusting scores for artefactual variants.


## Contents
- `/resys`: API main folder
- `/resys/__main__.py`: Top-level code to run the ASC3 folder (run app.py)
- `/resys/app.py`: Main module that runs FastAPI
- `/resys/models.py`: A inference model that predicts the probability of a confirmed mutation using query mutations and feature values of mutations
- `/resys/utils.py`: utils
- `/resys/logs`: log

```
.
├── resys
│   ├── __main__.py
│   ├── app.py
│   ├── models.py
│   ├── config.yaml
│   ├── routers.py
│   ├── utils.py
│   ├── logs
│   └── tests
├── README.md
└── requirements.txt
```


## How to use?
For server (Linux)
```
$ python3 resys
```

For client
```
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "sample_id": "TEST_SAMPLE",
    "inhouse_total_ac": 100,
    "gene_diseases": {
        "OMIM:600276-OMIM:125310": {
            "1-100-A-T": {
                "acmg_bayesian": 1,
                "qual": 1271.77,
                "ad": "287.27",
                "dp": 129.0,
                "disease_similarity": 3.09534946,
                "inhouse_variant_ac": 237
            },
            "1-200-A-T": {
                "acmg_bayesian": 0.99409,
                "qual": 1271.77,
                "ad": "287.27",
                "dp": 129.0,
                "disease_similarity": 5.09534946,
                "inhouse_variant_ac": 3
            }
        },
        "OMIM:12367-OMIM:23223": {
            "3-100-A-T": {
                "acmg_bayesian": 0.99409,
                "qual": 1271.77,
                "ad": "287.27",
                "dp": 129.0,
                "disease_similarity": -1.09534946,
                "inhouse_variant_ac": 237
            },
            "3-200-A-T": {
                "acmg_bayesian": 0.99409,
                "qual": 1271.77,
                "ad": "287.27",
                "dp": 129.0,
                "disease_similarity": -1.09534946,
                "inhouse_variant_ac": 237
            }
        }
    }
}
'
```



## Requirement
1. PyYAML
2. locust
3. Python3.7 ~
4. sklearn >= 0.24.2



## Author Affiliation
Research and Development Center, 3billion, 416 Teheran-ro, 06193 Seoul, Republic of Korea
