start:
	docker-compose up -d
stop:
	docker-compose down
migrate:
	alembic revision --autogenerate -m "Initial migration"
	alembic upgrade head
	sed -i 's/# speed = Column(Float)/speed = Column(Float)/g' reporting_client_v3.py
	alembic revision --autogenerate -m "Add speed field to Spaceship model"
	alembic upgrade head
scan:
	python3 reporting_client_v3.py scan 17 45 40.0409 -29 00 28.118

traitors:
	python3 reporting_client_v3.py list_traitors

.PHONY: start, stop, migrate, traitors, scan
