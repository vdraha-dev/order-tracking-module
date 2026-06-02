# order-tracking-module


# Запуск проекта


## Локально

```bash
pip install uv
uv sync
source .venv/bin/activate # Linux / macOS
.venv\Scripts\Activate.ps1 # Windows (PowerShell)
mkdir data
cp .env.example .env # Linux / macOS
Copy-Item .env.example .env # Windows (PowerShell)
alembic upgrade head
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
## Docker

```bash
docker compose up --build
```

# Docs

Після запуску проекта документація знаходиться за посиланням http://0.0.0.0:8000/docs#/


# SQL 

структуру таблиць можна переглянути за [посиланням](https://dbdiagram.io/d/6a1ee077f15b4b045257e638)

# Структура проекта

Дана структура проекта дозволяє розділення по доменах,
що полегшує маштабування.
Кожен домен дозволяє легко його версіонувати.


**UnitOfWork (uow.py)** групує репозиторії в одну транзакційну межу, а також гарантує consistency між кількома таблицями

**alembic** дозволяє версіонувати DB з історією змін

**config.py** ізоляція конфігурації від коду, pydantic_settings дозволяє автоматично завантажувати змінні середовища


```
.
├── alembic
├── alembic.ini
├── app
│   ├── core
│   │   ├── config.py
│   │   └── logging.py
│   ├── db
│   │   ├── base.py
│   │   └── session.py
│   ├── __init__.py
│   ├── main.py
│   ├── order_items
│   │   ├── models.py
│   │   └── repository.py
│   ├── orders
│   │   ├── api
│   │   │   └── v1
│   │   │       ├── router.py
│   │   │       └── schemas.py
│   │   ├── models.py
│   │   ├── repository.py
│   │   └── service.py
│   ├── products
│   │   ├── api
│   │   │   └── v1
│   │   │       ├── router.py
│   │   │       └── schemas.py
│   │   ├── models.py
│   │   ├── repository.py
│   │   └── service.py
│   ├── uow.py
│   └── users
│       ├── api
│       │   └── v1
│       │       ├── router.py
│       │       └── schemas.py
│       ├── models.py
│       ├── repository.py
│       └── service.py
├── data
├── database.db
├── docker-compose.yml
├── Dockerfile
├── image.png
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
```