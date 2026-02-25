#! /usr/bin/env bash
set -ex
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
root_path=$( cd "$(dirname $parent_path)" ; pwd -P )
cd $root_path/streamlit_app

python3 -m pip install click==8.1.7 boto3==1.34.16 six==1.16.0
python3 poetry_login.py --local false

docker compose up -d --build
