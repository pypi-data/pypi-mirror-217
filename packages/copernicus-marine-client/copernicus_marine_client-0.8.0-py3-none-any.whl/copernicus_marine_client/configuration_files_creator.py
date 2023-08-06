import base64
import logging
import os
from netrc import netrc
from typing import Tuple, Union

import click
import lxml.html
import requests


def retrieve_credentials_from_config_files(
    config_file_directory: str, host: str = "default_host"
) -> Tuple[Union[str, None], Union[str, None]]:

    username, password = None, None
    copernicus_marine_client_config_filename = os.path.join(
        config_file_directory, ".copernicus_marine_client_credentials"
    )
    netrc_type = "_netrc" if os.system == "win32" else ".netrc"
    netrc_filename = os.path.join(config_file_directory, netrc_type)
    motu_filename = os.path.join(
        config_file_directory, ".motuclient-python.ini"
    )
    if os.path.exists(copernicus_marine_client_config_filename):
        config_file = open(copernicus_marine_client_config_filename)
        config_lines = config_file.readlines()
        for line in config_lines:
            if line.startswith("username"):
                username = line.split("username=")[-1].strip()
            if line.startswith("password"):
                encoded_password = line.split("password=")[-1].strip()
                password = base64.standard_b64decode(encoded_password).decode(
                    "utf8"
                )
        if username and password:
            logging.debug(
                f"Credentials from {copernicus_marine_client_config_filename}"
            )
            return (username, password)

    elif os.path.exists(netrc_filename):
        authenticator = netrc(netrc_filename).authenticators(host=host)
        if authenticator:
            username, _, password = authenticator
            logging.debug(f"Credentials from {netrc_filename}")
            return (username, password)
    elif os.path.exists(motu_filename):
        motu_file = open(motu_filename)
        motu_lines = motu_file.readlines()
        for line in motu_lines:
            if line.startswith("user"):
                username = line.split("user=")[-1].strip()
            if line.startswith("pwd"):
                password = line.split("pwd=")[-1].strip()
        if username and password:
            logging.debug(f"Credentials from {motu_filename}")
            return (username, password)
    return (username, password)


def create_copernicus_marine_client_config_file(
    username: str, password: str, config_file_directory: str, assume_yes: bool
) -> None:
    encoded_password = base64.b64encode(password.encode("ascii", "strict"))
    config_lines = [
        f"username={username}\n",
        f"password={encoded_password.decode('utf-8')}\n",
    ]
    config_filename = os.path.join(
        config_file_directory, ".copernicus_marine_client_credentials"
    )
    if os.path.exists(config_filename) and not assume_yes:
        click.confirm(
            f"File {config_filename} already exists, overwrite it ?",
            abort=True,
        )
    config_file = open(config_filename, "w")
    config_file.writelines(config_lines)
    config_file.close()


def check_copernicus_marine_credentials(username: str, password: str):
    """
    Check provided Copernicus Marine Credentials are correct.

    Parameters
    ----------
    username : str
        Copernicus Marine Username, provided for free from https://marine.copernicus.eu
    password : str
        Copernicus Marine Password, provided for free from https://marine.copernicus.eu

    """
    cmems_cas_url = "https://cmems-cas.cls.fr/cas/login"
    conn_session = requests.session()
    login_session = conn_session.get(cmems_cas_url)
    login_from_html = lxml.html.fromstring(login_session.text)
    hidden_elements_from_html = login_from_html.xpath(
        '//form//input[@type="hidden"]'
    )
    playload = {
        he.attrib["name"]: he.attrib["value"]
        for he in hidden_elements_from_html
    }
    playload["username"] = username
    playload["password"] = password
    response = conn_session.post(cmems_cas_url, data=playload)
    if response.text.find("success") == -1:
        credential_error_message = ConnectionRefusedError(
            "Incorrect username or password.\n"
            "Learn how to recover your credentials at: "
            "https://help.marine.copernicus.eu/en/articles/"
            "4444552-i-forgot-my-username-or-my-password-what-should-i-do"
        )
        logging.error(credential_error_message)
        raise credential_error_message


def main(
    username: str, password: str, config_file_directory: str, assume_yes: bool
) -> None:
    if not os.path.exists(config_file_directory):
        os.makedirs(config_file_directory)
    create_copernicus_marine_client_config_file(
        username=username,
        password=password,
        config_file_directory=config_file_directory,
        assume_yes=assume_yes,
    )
