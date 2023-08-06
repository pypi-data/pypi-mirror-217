# DashIQ Lib

This repository is hosts DashIQ's python library.

## Running tests locally

1. Clone the repo
2. Create a new virtual environment
3. Install with the extra test dependencies w/ `pip install -e .[tests]` (note, if you use zsh you will have to escape the brackets i.e. `\[tests\]`)
4. Run the tests: `pytest --cov --cov-report term-missing:skip-covered`. Alternatively run `make tests`

