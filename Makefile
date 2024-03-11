migrate:
	docker compose exec app python src/manage.py migrate $(if $m, api $m,)

makemigrations:
	python src/manage.py makemigrations

createsuperuser:
	docker compose exec app python src/manage.py createsuperuser

docker:
	docker compose up --build

lint:
	isort .
	flake8 --config setup.cfg
	black --config pyproject.toml .

check_lint:
	isort --check --diff .
	flake8 --config setup.cfg
	black --check --config pyproject.toml .
