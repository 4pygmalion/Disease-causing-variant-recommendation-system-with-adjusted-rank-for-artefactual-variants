# Disease-causing variant recommendation system for Rare diseases 

: API containing a disease-causing variant recommendation system that integrates quality control into variant prioritization by adjusting scores for artefactual variants.


## Contents
- `/resys`: 변이추천시스템의 구동 폴더
- `/resys/__main__.py`: ASC3 폴더를 동작시기 위한 최상위 코드 (app.py을 구동)
- `/resys/app.py`: FastAPI을 동작시키는 메인 모듈
- `/resys/models.py`: 쿼리 변이들과 변이들의 특징값을 인자로하여 컨펌 변이의 확률을 추론하는 추론기
- `/resys/utils.py`: 로깅과 YAML파일을 로딩하는 유틸
- `/resys/logs`: 로그 폴더

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


## Requirement
1. PyYAML
2. locust
3. Python3.7 ~
4. sklearn >= 0.24.2

## Install
TODO


## How to use?
For server (Linux)
```
$ python3 ASC3
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

# 
Research and Development Center, 3billion, 416 Teheran-ro, 06193 Seoul, Republic of Korea
