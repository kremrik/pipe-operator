run-test :
	@python3 -m pytest

type-check :
	@mypy pipe

coverage :
	@coverage run -m unittest tests/test*.py
	@coverage html
	@python3 -m http.server 8000 --directory htmlcov/