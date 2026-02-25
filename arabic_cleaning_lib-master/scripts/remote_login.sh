#! /usr/bin/env bash

export POETRY_HTTP_BASIC_MOZN_PASSWORD=$(aws \
    --no-cli-pager --region 'eu-central-1' \
    codeartifact get-authorization-token \
    --domain mozn --domain-owner 947865815790 \
    --query authorizationToken --output text)
export POETRY_HTTP_BASIC_MOZN_USERNAME=aws
