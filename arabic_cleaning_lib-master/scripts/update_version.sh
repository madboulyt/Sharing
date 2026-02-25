#! /usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e

if [ -z "$1" ]; then
    echo "No argument supplied. You must supply the new version as an argument"
    exit 1
else
    # Note that the input is in the form of vx.x.x so we remove the v because we don't need it
    version_number=$(echo "$1" | sed "s/^v//")
fi

if [ -z "$2" ]; then
    echo "No argument supplied. You must supply a true or false as an argument"
    exit 1
fi

# Update pyproject.toml version
if [ "$(uname)" == "Darwin" ]; then
    # NOTE: On MacOS which uses BSD sed (instead of GNU sed) you need to specify the backup extension (e.g. ".old")
    sed -i .old 's/^version = \".*\"$/version = \"'$version_number'\"/' pyproject.toml
    sed -i .old 's/^__version__ = \".*\"$/__version__ = \"'$version_number'\"/' arabic_cleaning/__init__.py
    rm pyproject.toml.old
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    sed -i 's/^version = \".*\"$/version = \"'$version_number'\"/' pyproject.toml
    sed -i 's/^__version__ = \".*\"$/__version__ = \"'$version_number'\"/' arabic_cleaning/__init__.py
else
    echo "Unsupported Platform $(uname)"
    exit 1
fi

git add pyproject.toml arabic_cleaning/__init__.py

if [ "$2" == "false" ]; then
    # Update Image tag version
    if [ "$(uname)" == "Darwin" ]; then
        # NOTE: On MacOS which uses BSD sed (instead of GNU sed) you need to specify the backup extension (e.g. ".old")
        sed -i .old 's/^IMAGE_TAG=.*$/IMAGE_TAG=v'$version_number'/' .env
        rm .env.old
        git add .env
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        sed -i 's/^IMAGE_TAG=.*$/IMAGE_TAG=v'$version_number'/' .env
        git add .env
    else
        echo "Unsupported Platform $(uname)"
        exit 1
    fi
fi
