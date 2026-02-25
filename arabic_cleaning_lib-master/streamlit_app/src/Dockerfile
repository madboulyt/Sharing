ARG ECR_PYTHON
ARG PYTHON_TAG
FROM $ECR_PYTHON:$PYTHON_TAG AS base-image

WORKDIR /backend

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY cleaning_streamlit-*.auth.toml /root/.config/pypoetry/auth.toml
COPY ./poetry.lock ./pyproject.toml /backend
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root  ; else poetry install --no-root --no-dev ; fi"

COPY ./ /backend
