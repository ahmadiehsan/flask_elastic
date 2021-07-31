FLASK_ENV=development
FLASK_APP=src/app.py

start_dev:
	FLASK_ENV=$(FLASK_ENV) FLASK_APP=$(FLASK_APP) flask run

db_create_migrate_version:
	cd migrations; FLASK_ENV=$(FLASK_ENV) PYTHONPATH=.. alembic revision --autogenerate -m $(filter-out $@,$(MAKECMDGOALS))

db_migrate:
	cd migrations; FLASK_ENV=$(FLASK_ENV) PYTHONPATH=.. alembic upgrade head

db_fake_migrate:
	cd migrations; FLASK_ENV=$(FLASK_ENV) PYTHONPATH=.. alembic stamp head
