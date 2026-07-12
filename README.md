# Ingestão de Dados do TSE

Extrai os dados dos dados abertos do TSE e faz a ingestão para o S3 na camada landing.

### Stach Utilizada

- Storage: S3
- Orquestrador: Lambda
- Infra: Terraform
- Linguagem: Python
- Ambiente: Poetry

## Base Utilizadas

- 
- 
- 
- 
- 

### Estrutura do projeto
tse-data-ingestion/
│
├── README.md
├── pyproject.toml
├── poetry.lock
├── .env
│
├── src/ 
│   ├── shared.py
│   │
│   ├── extract/
│   │   ├── downloader.py
│   │   └── lambda_extract.py
│   │
│   ├── bronze/
│   │   ├── unzipper.py
│   │   └── lambda_bronze.py
│   │
│   └── pipeline/
│       └── orchestrator.py
│
├── infra/
│       ├── s3.tf
│       ├── lambda.tf
│       │
│       └── iam.tf
└── scripts/
    ├── local_run.py
    └── debug_pipeline.py