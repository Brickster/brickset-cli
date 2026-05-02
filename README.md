# brickset CLI

[![build](https://github.com/Brickster/brickset-cli/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/Brickster/brickset-cli/actions/workflows/build.yml) [![Maintainability](https://qlty.sh/gh/Brickster/projects/brickset-cli/maintainability.svg)](https://qlty.sh/gh/Brickster/projects/brickset-cli) [![Code Coverage](https://qlty.sh/gh/Brickster/projects/brickset-cli/coverage.svg)](https://qlty.sh/gh/Brickster/projects/brickset-cli)

A command line interface for [brickset](https://brickset.com)'s [v3 API](https://brickset.com/article/52664/api-version-3-documentation).

## Requirements
- Python 3.10+

## Installation

```commandline
$ python3.10 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

```commandline
$ brickset config YOUR_API_KEY
$ brickset login
# prompted for username/password to retrieve a user hash
```

## Running tests

```commandline
$ pip install -r requirements-test.txt
$ pytest tests/
```
