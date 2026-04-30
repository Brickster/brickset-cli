# brickset CLI

[![Python application](https://github.com/Brickster/brickset-cli/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/Brickster/brickset-cli/actions/workflows/python-app.yml)

A command line interface for [brickset](https://brickset.com)'s [v3 API](https://brickset.com/article/52664/api-version-3-documentation).

## Requirements
- Python 2.7+

## Installation

```commandline
$ python3 -m venv .venv
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
