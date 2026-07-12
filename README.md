# Customer Accounts Microservice

[![CI Build](https://github.com/nehhub2024/accounts/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/nehhub2024/accounts/actions)
[![codecov](https://codecov.io/gh/nehhub2024/accounts/branch/main/graph/badge.svg)](https://codecov.io/gh/nehhub2024/accounts)

## Overview

This project is a RESTful microservice for managing **Customer Accounts**.
It was built as the capstone project for the DevOps and Software Engineering
specialization, applying Agile planning, Test-Driven Development, Continuous
Integration, application security, containerization, and Continuous
Deployment to Kubernetes.

## Contents

```text
accounts/
├── .github/workflows/
│   └── ci-build.yaml        # GitHub Actions CI workflow
├── k8s/
│   ├── deployment.yaml       # Kubernetes Deployment for the service
│   ├── service.yaml          # Kubernetes Service (NodePort, port 8080)
│   └── postgresql.yaml       # Postgres Deployment/Service/Secret
├── tekton/
│   ├── pipeline.yaml         # Tekton CD Pipeline definition
│   └── pipelinerun.yaml      # Tekton PipelineRun trigger
├── service/
│   ├── __init__.py           # App factory, Talisman + CORS setup
│   ├── config.py             # Configuration from environment
│   ├── models.py             # Account SQLAlchemy model
│   ├── routes.py             # REST API routes (CRUD)
│   └── common/
│       ├── status.py         # HTTP status code constants
│       ├── error_handlers.py # JSON error handlers
│       └── log_handlers.py   # Gunicorn logging integration
├── tests/
│   ├── factories.py          # factory-boy fake data generator
│   ├── test_models.py        # Unit tests for the Account model
│   └── test_routes.py        # Integration tests for the REST API
├── Dockerfile
├── requirements.txt
├── setup.cfg                 # nosetests / coverage / flake8 / pylint config
└── user-story.md             # User story template
```

## API Endpoints

| Method | URL                  | Description               |
|--------|----------------------|----------------------------|
| GET    | `/`                  | Root URL / service info    |
| GET    | `/health`            | Health check                |
| POST   | `/accounts`          | Create a new Account        |
| GET    | `/accounts`          | List all Accounts           |
| GET    | `/accounts/{id}`     | Read an Account              |
| PUT    | `/accounts/{id}`     | Update an Account            |
| DELETE | `/accounts/{id}`     | Delete an Account            |

## Running Locally

```bash
pip install -r requirements.txt
python3 -c "from service import app; app.run(host='0.0.0.0', port=8080)"
```

## Running the Tests

```bash
nosetests --with-spec --spec-color -v
```

## Running with Docker

```bash
docker build -t accounts:1.0 .
docker run -d --name accounts -p 8080:8080 accounts:1.0
```

## Deploying to Kubernetes

```bash
kubectl apply -f k8s/postgresql.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get deployments,pods,rs,svc
```

## License

Licensed under the Apache License. See [LICENSE](LICENSE) for more
information.
