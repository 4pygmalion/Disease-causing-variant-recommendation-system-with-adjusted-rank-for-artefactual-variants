# Confirmed Variant Recommendation System (ASC3)
Disease similarity (22-3Q-OKR13) 
: API to calcualting disease similarity to server GEBRA webpage using TCP socket (https://gebra.io). API requires three data modal including ACMG baysian score, semantic simiarity based on HPO ontology, and etc With these scores, model based on linear regression return disesase similartiy score. 


## Contents
- `/ASC3`: 변이추천시스템의 구동 폴더
- `/ASC3/__main__.py`: ASC3 폴더를 동작시기 위한 최상위 코드 (app.py을 구동)
- `/ASC3/app.py`: FastAPI을 동작시키는 메인 모듈
- `/ASC3/models.py`: 쿼리 변이들과 변이들의 특징값을 인자로하여 컨펌 변이의 확률을 추론하는 추론기
- `/ASC3/utils.py`: 로깅과 YAML파일을 로딩하는 유틸
- `/ASC3/logs`: 로그 폴더
- `/validation`: Validation 샘플과 모델 서치를 하기 위한 폴더
- `/anaylsis_code`: 통계량 분석을 위한 ipynb을 담고 있는 폴더
```
.
├── ASC3
│   ├── __main__.py
│   ├── app.py
│   ├── models.py
│   ├── config.yaml
│   ├── routers.py
│   ├── utils.py
│   ├── logs
│   └── tests
├── anaylsis_code
├── backup
├── data
│   └── validation_samples
├── README.md
├── requirements.txt
└── validation
    ├── config.yaml
    ├── mlruns
    ├── model_search_with_mlflow.py
    ├── tests
    ├── validation_samples_generator.py
    ├── validation_utils.py
    └── validator.py
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


## Credit
- Heon
- Isaac
- Tyler
- Kyle 

Reviwed by seom, jame


## License
todo
