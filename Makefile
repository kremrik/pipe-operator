.PHONY: test
test :
	@python3 -m pytest

.PHONY: type-check
type-check :
	@mypy pipe

.PHONY: coverage
coverage :
	@coverage run -m unittest tests/test*.py
	@coverage html
	@python3 -m http.server 8000 --directory htmlcov/

.PHONY: set-hooks
set-hooks:
	@git config core.hooksPath .githooks
	@chmod +x .githooks/*
