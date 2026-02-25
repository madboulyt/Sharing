# Mozn Arabic cleaning library

## Table of contents
- [Project Structure](#project-structure)
- [Example usage](#example-usage)
- [Download the requirements](#download-the-requirements)
- [Configure AWS CLI](#configure-aws-cli)
- [Run Docker script](#run-docker-script)
- [Install pre commit](#install-pre-commit)
- [Installing the library in another project](#installing-the-library-in-another-project)
- [To do](#to-do)

## Project Structure
The library contains 3 main files for usage and a constants module:
- `text_cleansing.py`:
This contains functions that would clean and fix Arabic strings. It's should be applied to every Arabic text before applying the filters.
from common
- `quality_filters.py`:
This contains functions that applies certain stats on the text and return whether the filter conditions are passed or not. It expects a document to be represented as list of lists of strings (Splits document by new line character '\n' and then by space character, a helper function to do that exits in `cleaning_utils.py`).
- `cleaning_utils.py`:
Contains the following helper functions:
	* `doc_to_lines(doc)`: Split a document by new line character '\n' and then by space character. Used before passing to quality_filters.
	* `cleanse_document(doc, cleansers)`: Given a string document and a list of cleanser functions (from `text_cleansing.py` or custom made), it applies the cleansing functions on the string.
    * `filter_document(doc, filters)`: Given a list of lists of strings (output of `doc_to_lines`) document and a list of filters functions (from `quality_filters.py` or custom made), it applies the filter functions on the document.
    * `chunck_document(doc,chunk_max_size, sep, apply_backward_stepping)`:
    * `def clean_and_filter_docs(docs, cleansers, filters, n_jobs)`:
    * `clean_and_filter_json_docs(in_jsonl_path, text_field, out_jsonl_path, cleansers, filters, n_jobs)`:
- constents: Contains many constents related to the Arabic filters and cleaning scripts
## Example usage

### Example 1
The simplist example usage is to prepare a jsonl document and call the function `clean_and_filter_json_docs` like this:
```python
from arabic_cleaning.cleaning_utils import clean_and_filter_json_docs
clean_and_filter_json_docs(
	in_jsonl_path="documents.jsonl",
	text_field="text",
	out_jsonl_path="output_docs.jsonl",
)
```
This will apply the default filters (with default parameters) and cleaners to the file `documents.jsonl` and produces the file `output_docs.jsonl` where only the documents that passed all the filters will be there after they have been cleaned.
If only the cleansing is wanted, the filters argument can have an empty list:
```python
from arabic_cleaning.cleaning_utils import clean_and_filter_json_docs
clean_and_filter_json_docs(
	in_jsonl_path="documents.jsonl",
	text_field="text",
	out_jsonl_path="output_docs.jsonl",
	filters=[],
)
```
This will only clean the documents without dropping any document.

### Example 2
Cleaning a list of strings can be done using the function `clean_and_filter_docs` like this:
```python
from arabic_cleaning.cleaning_utils import clean_and_filter_docs
clean_and_filter_docs(docs=[
	"مصطفي\n\n\nمحمد\n\n\nmostafa\n\n\nmohamed.\n\n\nمحمود",
	"ذهب محمد الي  ss ss ss ss ss ss ss سيdd",
	])
```
This will apply the default filters (with default parameters) and cleaners to the documents where only the documents that passed all the filters will be returned after they have been cleaned.

## Download the requirements

First, make sure you have installed all the requirements in your machine:

* [git](https://formulae.brew.sh/formula/git).
* [Docker](https://docs.docker.com/docker-for-mac/install/).
* [AWS CLI](https://formulae.brew.sh/formula/awscli).
* [docker-credential-helper-ecr](https://formulae.brew.sh/formula/docker-credential-helper-ecr).


## Configure AWS CLI

Create a directory with the name `.aws` inside your home directory

```bash
mkdir ~/.aws
```

Copy the content of [this aws config file](https://github.com/MoznSystems/infrastructure/blob/master/aws_terraform/modules/generate_aws_config/package/aws_config) to your machine in `~/.aws/config`

> Note: if you get a 404 error message, that means you don't have access to the [infrastructure repo](https://github.com/MoznSystems/infrastructure), ask another engineer to send you the content of the [the aws config file](https://github.com/MoznSystems/infrastructure/blob/master/aws_terraform/modules/generate_aws_config/package/aws_config) because it's all you need.

Login into aws

```bash
aws sso login --profile sso-nlp-research-dev-access
```

## Run Docker script

You can use docker to interact with the images directly, or you can use `./scripts/run_docker.sh` which bundles usefull commands and is easier to use.

### Build image
`./scripts/run_docker.sh local build-image`

### Update dependencies
`./scripts/run_docker.sh local lock`
Although that is not a good idea. Better to update the pyproject.toml file. Submit a PR.
The bot will update the lock for you saving a lot of time.

### Run the container and wait
`./scripts/run_docker.sh local up`

### Stop the container
`./scripts/run_docker.sh local stop`

### Run tests
`./scripts/run_docker.sh local pytest`

or to run continuously and watch for changes in files
`./scripts/run_docker.sh local ptw`

### Run jupyterlab
`./scripts/run_docker.sh local jupyter`
you can see the ports from the script.

### Other commands
please refer to the script.

## Install pre commit
assumeing you have pre-commit on your machine
`pre-commit install --overwrite --install-hooks`

Now you will not be allowed to commit if you don't comply with formatting and linting rules.

Subsequently to run it the first time
`pre-commit run --all-files`

## Installing the library in another project
Before installing, you need to login into AWS sso using:
```bash
aws sso --profile sso-nlp-research-dev-access
```

To install `arabic_cleaning` library in any project use of following methods:

### Poetry installation
Steps to add library:
- Add the package to the dependency requirements in the `pyproject.toml` file
```mozn-arabic-cleaning = "1.1.3"```
- Add the AWS Codeartifcat source to `pyproject.toml` :
```toml
[[tool.poetry.source]]
name = "mozn"
url = "https://mozn-947865815790.d.codeartifact.eu-central-1.amazonaws.com/pypi/general/simple/"
```
- Use the script at `scripts/local_login.sh` to generate credentials
for accessing AWS codeartifcat
- Configure poetry to use the AWS Codeartifact to download packages
```bash
poetry config http-basic.mozn $POETRY_HTTP_BASIC_MOZN_USERNAME $POETRY_HTTP_BASIC_MOZN_PASSWORD
```
- Create a new lock file `poetry lock` and install the package `poetry install` like usual


### Install directly from repo using pip
- Clone this repo in your machine
- Check out the tag you want to install
```bash
git fetch --tags && git checkout v1.1.3
```
- Inside the repo run this (It's better to do it within a virtual env):
```bash
pip install .
```

### Pip installation (Not working on all machines yet)
This method is pending cross compiling for the library to work
on all platforms:
- Add the package to the dependency requirements in the `requirements.txt` file
```mozn-arabic-cleaning==1.1.3```
- Run this command to create credentials for AWS CodeArtificat
```bash
aws --profile sso-nlp-research-dev-access codeartifact login --tool pip --repository general --domain mozn --domain-owner 947865815790 --region eu-central-1
```
Note: This might confiugre your pip globably to alwasy AWS CodeArtifcat and to disable that just delete the file `~/.config/pip/pip.conf`

- Run the installation command `pip install -r requirements.txt`

## To do
- Implement parallel cleaning and parallel filtering
- Add more tests to cover all the code
- Refactor all the regex in the `text_cleansing.py`
