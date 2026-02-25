#! /usr/bin/env python3

import os
import shutil
from datetime import datetime, timedelta
from glob import glob
from hashlib import md5
from textwrap import dedent
from typing import List, Optional

import boto3
import click


def auth(session: Optional[boto3.Session] = None):
    if session is None:
        session = boto3.session.Session(region_name="eu-central-1")

    codeartifact = session.client("codeartifact")
    auth_token = codeartifact.get_authorization_token(
        domain="mozn", domainOwner="947865815790"
    )["authorizationToken"]
    return "aws", auth_token


def local_auth(profile_name: str, region_name: Optional[str] = None):
    if region_name is None:
        # Default region for all of Mozn
        region_name = "eu-central-1"

    session = boto3.session.Session(region_name=region_name, profile_name=profile_name)
    return auth(session)


def generate_poetry_auth_file(
    project_name: str,
    dependencies_hash: str,
    timeout: int,
    local: bool,
    profile_name: str,
):
    if local:
        username, password = local_auth(profile_name=profile_name)
    else:
        username, password = auth()
    poetry_auth_file_contents = dedent(
        f"""\
    [http-basic]
    [http-basic.mozn]
    username = \"{username}\"
    password = \"{password}\"
    """
    )
    new_auth_file = f"/var/tmp/{project_name}-{timeout}-{dependencies_hash}.auth.toml"
    with open(new_auth_file, "wt") as fd:
        fd.write(poetry_auth_file_contents)

    print(f"Created new auth file {new_auth_file}")
    return new_auth_file


def _md5sum(txt, is_file=True):
    if is_file:
        with open(txt, mode="rb") as fd:
            txt = fd.read()
    return md5(txt).hexdigest()


def login(
    local: bool,
    project_name: str,
    pyproject_paths: List[str],
    profile_name: str,
    cred_paths: Optional[List[str]],
):
    auth_files = list(glob(f"/var/tmp/{project_name}-*.auth.toml"))

    auth_file = None
    if len(auth_files) > 1:
        for file in auth_files:
            os.remove(file)
        print(
            f"Found multiple auth files ({auth_files}), deleting them and creating a new one"
        )
    elif len(auth_files) == 1:
        auth_file = auth_files[0]

    hashes = []
    for path in pyproject_paths:
        hashes.append(_md5sum(f"{path}/pyproject.toml"))
        hashes.append(_md5sum(f"{path}/poetry.lock"))
    current_dependencies_hash = _md5sum("".join(hashes).encode("utf-8"), is_file=False)
    new_timeout = int(datetime.timestamp(datetime.utcnow() + timedelta(hours=12)))

    new_auth_file = None
    if auth_file is not None:
        print(f"Found auth file {auth_file}")
        _, auth_timeout, old_dependencies_hash = (
            os.path.basename(auth_file).split(".auth.toml")[0].split("-")
        )
        auth_timeout = datetime.fromtimestamp(int(auth_timeout))

        # We check for poetry.lock hashes to ensure that we never re-install dependencies unless the dependencies have changed
        if (
            current_dependencies_hash != old_dependencies_hash
            and auth_timeout <= datetime.utcnow()
        ):
            new_auth_file = generate_poetry_auth_file(
                project_name=project_name,
                dependencies_hash=current_dependencies_hash,
                timeout=new_timeout,
                local=local,
                profile_name=profile_name,
            )

            os.remove(auth_file)
            print(f"Removing existing auth file {auth_file}")
        else:
            print(f"You are already authenticated with {auth_file}, nothing to do")
            new_auth_file = auth_file
    else:
        print("Failed to find an existing auth file, creating a new one")
        new_auth_file = generate_poetry_auth_file(
            project_name=project_name,
            dependencies_hash=current_dependencies_hash,
            timeout=new_timeout,
            local=local,
            profile_name=profile_name,
        )
    if cred_paths is not None:
        for cred_path in cred_paths:
            for file in glob(f"{cred_path}/{project_name}-*.auth.toml"):
                os.remove(file)
        for cred_path in cred_paths:
            shutil.copy(new_auth_file, cred_path)
    return new_auth_file


@click.command()
@click.option("--local", default=True, help="Run command with okta")
@click.option(
    "--project_name",
    default="cleaning_streamlit",
    required=True,
    help="Project name to store in /var/tmp/{project_name}",
)
@click.option(
    "--pyproject_paths",
    required=True,
    default=["./src"],
    help="list of paths to finde pyproject.toml and poetry.lock",
    multiple=True,
)
@click.option(
    "--profile_name",
    default="sso-shared",
    required=True,
    help="To be used for okta auth",
)
@click.option(
    "--cred_paths",
    default=["./src"],
    required=False,
    help="Path to copy generated creditionals to",
    multiple=True,
)
def login_cli(
    local: bool,
    project_name: str,
    pyproject_paths: List[str],
    profile_name: str,
    cred_paths: Optional[List[str]],
):
    login(local, project_name, pyproject_paths, profile_name, cred_paths)


if __name__ == "__main__":
    login_cli()
    # Run the script like this to generate the cred files
    # --profile_name sso-osos-platform-access --cred_paths ./backend
