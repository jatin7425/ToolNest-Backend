lint-fix:
	black .

test:
	python -m pytest --reuse-db

test-reset:
	python -m pytest --create-db
