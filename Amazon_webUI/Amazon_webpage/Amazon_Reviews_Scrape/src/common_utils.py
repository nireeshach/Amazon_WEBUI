""" Common functions used in project """

import os
from typing import List

import requests
import pandas
import urllib3
from lxml import html

# Disabling InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CustomeError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


def get_response(url: str) -> dict:
    """ Function which takes URL as input and returns HTML dom response

    Args:
        url(str): Url to get the HTTP response and construct HTML dom from the response
    Returns:
        dict: Dictonary with error message if any and HTML dom (lxml.html.HtmlElement)
    """

    resp_data = {"error": None, "doc": None}
    # Adding user agent to prevent amazon from blocking the request
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, verify=False, timeout=30)
    if response.status_code == 404:
        resp_data["error"] = "No webpage found for the given url: {}".format(url)
        return resp_data

    if response.status_code != 200:
        resp_data["error"] = "Failed to get response from the given url: {}, Status: {}".format(url, response.status_code)
        return resp_data

    if "Sorry, we just need to make sure you" in response.text:
        resp_data[
            "error"
        ] = "Requests are blocked from this IP, please try from other network!"
        return resp_data

    # Removing the null bytes from the response.
    cleaned_response = response.text.replace("\x00", "")

    with open("testresponse.html", "w") as f:
        f.write(cleaned_response)

    resp_data["doc"] = html.fromstring(cleaned_response)
    return resp_data


def write_data(feed_data: List, output_file: str, columns: List = []):
    """ Function to write List of dicts with entry values to CSV file

    Args:
        feed_data(list): List of dicts
        output_file(str): Outfile name
        columns(list): List of column names

    Returns:
    """
    if os.path.isfile(output_file):
        mode = "a"
    else:
        mode = "w"

    if columns:
        df = pandas.DataFrame(feed_data, columns=columns)
    else:
        df = pandas.DataFrame(feed_data)

    csv_params = {"index": False}
    if mode == "a":
        csv_params["header"] = False
    if columns:
        csv_params["columns"] = columns

    with open(output_file, mode) as f:
        df.to_csv(f, **csv_params)
