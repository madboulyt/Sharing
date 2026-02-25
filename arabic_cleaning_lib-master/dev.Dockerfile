ARG ECR_REPO
ARG IMAGE_TAG
ARG ECR_PYTHON
ARG PYTHON_TAG

FROM $ECR_PYTHON:$PYTHON_TAG as python-base
ARG APP_PATH

FROM python-base as development
ARG APP_PATH
ARG POETRY_HTTP_BASIC_MOZN_USERNAME
ARG POETRY_HTTP_BASIC_MOZN_PASSWORD
WORKDIR $APP_PATH
COPY --from=python-base $POETRY_HOME $POETRY_HOME
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root
RUN poetry config http-basic.mozn $POETRY_HTTP_BASIC_MOZN_USERNAME $POETRY_HTTP_BASIC_MOZN_PASSWORD
ENTRYPOINT ["/bin/sh", "-c"]

FROM development as testing
COPY poetry.lock pyproject.toml ./
COPY tests ./tests
COPY arabic_cleaning ./arabic_cleaning
COPY README.md ./
RUN poetry run pytest -v
RUN poetry build -f wheel

FROM $ECR_PYTHON:$PYTHON_TAG as test-built
ARG APP_PATH
COPY --from=testing $APP_PATH/dist/*.whl .
ARG POETRY_HTTP_BASIC_MOZN_USERNAME
ARG POETRY_HTTP_BASIC_MOZN_PASSWORD
RUN pip config set global.index-url https://$POETRY_HTTP_BASIC_MOZN_USERNAME:$POETRY_HTTP_BASIC_MOZN_PASSWORD@mozn-947865815790.d.codeartifact.eu-central-1.amazonaws.com/pypi/general/simple/
RUN pip install *.whl
RUN pip install pytest
COPY tests tests
RUN pytest -v tests/
RUN touch success

FROM testing as publish
COPY --from=test-built success .
ARG POETRY_HTTP_BASIC_MOZN_USERNAME
ARG POETRY_HTTP_BASIC_MOZN_PASSWORD
RUN poetry publish -u $POETRY_HTTP_BASIC_MOZN_USERNAME -p $POETRY_HTTP_BASIC_MOZN_PASSWORD -r mozn-upload
