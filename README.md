# Blog Rest-API Project (Flask + Elasticsearch)

### Goal

In this project I have tried to use low-level libraries,
so libraries like Flask-SQLAlchemy, Flask-Migrate or Flask-Alembic have been ignored.

### Prerequisites

- Elasticsearch (7.9.2)
- Make (`apt install make`)

### Quick Run

```
pip install -r requirements.txt
make db_migrate
make start_dev
```

visit [http://localhost:5000/api/docs](http://localhost:5000/api/docs)

### Management Commands

usage: `make <COMMAND_NAME>` 

- start_dev
- db_create_migrate_version <MIGRATION_NAME>  # e.x. make db_create_migrate_version remove_email_field
- db_migrate
- db_fake_migrate

