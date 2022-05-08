"""Perform webscraping related to typosquatting on PyPI.

A module that contains any functions that can make internet
calls to gather data related to typosquatting.
"""

import json
import sys
import urllib.request

from bs4 import BeautifulSoup
import requests
import jsontree

import constants

TOP_N = constants.TOP_N


def get_all_packages(page="https://pypi.org/simple/"):
    """Download simple list of PyPI package names.

    pypi.org/simple conveniently lists all the names of current
    packages. This function scrapes that listing and then places
    the package names in a python list structure.

    Args:
        page (str): webpage from which to download pypi package names

    Returns:
        list: package names on pypi
    """
    # Retrieve package name listing data from pypy
    try:
        pypi_package_page = requests.get(page)
    except requests.exceptions.ConnectionError as e:
        print("Internet connection issue. Check connection")
        print(e)
        sys.exit(1)

    # Convert html to easily digestible format
    soup = BeautifulSoup(pypi_package_page.text, "html.parser")

    # Store package names in list
    package_names = []
    for elem in soup.find_all("a"):  # Find all <a> tags
        package_names.append(elem.string)  # Get string inside a tag

    # Return timestamp and package name list
    return package_names


def get_top_packages(top_n=TOP_N, stored=False):
    """Identify top packages by download count on pypi.

    A friendly person has already provided an occasionally
    updated JSON feed to enable this program to build a list
    of the top pypi packages by download count. The default
    does a fresh pull of this feed. If the user wants to use
    a stored list, that is possible if the user sets the stored
    flag to true.

    Args:
        top_n (int): the number of top packages to retrieve
        stored (bool): whether to use the stored package list

    Returns:
        dict: top packages
    """
    if stored:  # Get stored data
        with open("top_packages_may_2020.json", "r") as f:
            data = json.load(f)
    else:  # Get json data for top pypi packages from website
        top_packages_url = (
            "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.json"
        )
        # Catch if internet connectivity causes failure
        try:
            with urllib.request.urlopen(top_packages_url) as url:  # nosec
                data = json.loads(url.read().decode())
        except urllib.error.URLError as e:
            print("Internet connection issue. Check connection")
            print(e)
            sys.exit(1)

    # Make JSON data easy to navigate
    json_data = jsontree.jsontree(data)

    # Place top_n packages in dict, where key is package
    # name and value is rank
    top_packages = {}
    for i in range(0, top_n):
        package_info = json_data.rows[i]
        package_name = package_info["project"]
        top_packages[package_name] = i + 1

    return top_packages


def get_metadata(name):
    """Retrieve pypi package metadata for one package.

    Retrieve via an internet call to PyPI via JSON metadata on a particular
    PyPI package and return this information.

    Args:
        name (str): name of package on pypi for which to retrieve metadata

    Returns:
        dict: package metadata
    """
    try:
        # Make call to specified PyPI package via API endpoint
        link = "https://pypi.org/pypi/" + name + "/json"
        response = requests.get(link)

        # Convert JSON to dict
        metadata_dict = response.json()
    except json.decoder.JSONDecodeError as e:
        metadata_dict = {
            "info": {
                "author_email": "",
                "author": "",
                "package_url": "",
                "description": "",
                "home_page": "",
                "summary": "",
            }
        }

    # Return dict version
    return metadata_dict
