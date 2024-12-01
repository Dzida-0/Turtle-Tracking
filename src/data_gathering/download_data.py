import json
import logging
import os
from typing import Optional, Dict
import requests


def check_connection() -> Dict[bool, str]:
    """
    Check if there is an internet connection by pinging Google's website.
    :return: dictionary with key True and empty value if successfully connected,
     otherwise False as key and error name as value.
    """
    try:
        response = requests.get("https://www.google.com", timeout=3)
        response.raise_for_status()
        return {True: ""}
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error occurred: {err}")
        return {False: f"HTTP error occurred: {err}"}
    except requests.Timeout as err:
        logging.error(f"Timeout error occurred: {err}")
        return {False: f"Timeout error occurred: {err}"}
    except requests.exceptions.RequestException as err:
        logging.error(f"Request error occurred: {err}")
        return {False: f"Request error occurred: {err}"}


def download_turtles_info() -> Dict[bool, str]:
    """
    Download all information about turtles (name, species, ect.)
    :return: dictionary with key True and empty value if successfully connected,
     otherwise False as key and error name as value.
    """
    if not check_connection():
        logging.warning("No internet connection")
        return {False: "No internet connection"}
    url = "https://stc.mapotic.com/api/v1/poi/"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        os.makedirs("../data/raw", exist_ok=True)
        with open("../data/raw/turtles_info.json", "w") as f:
            json.dump(data, f)
        return {True: ""}

    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error occurred: {err}")
        return {False: f"HTTP error occurred: {err}"}
    except requests.Timeout as err:
        logging.error(f"Timeout error occurred: {err}")
        return {False: f"Timeout error occurred: {err}"}
    except requests.exceptions.RequestException as err:
        logging.error(f"Request error occurred: {err}")
        return {False: f"Request error occurred: {err}"}
    except ValueError:
        logging.error("Failed to decode JSON from response")
        return {False: "Failed to decode JSON from response"}


def download_turtles_positions(turtle_id: int, positions_quantity: Optional[int] = 10000) -> Dict[bool, str]:
    """
    Download all position and movement related information for given turtle
    :param turtle_id: ID number of turtle
    :param positions_quantity: Amount of last positions to be downloaded (all if not provided).
    :return: dictionary with key True and empty value if successfully connected,
     otherwise False as key and error name as value.
    """
    if not check_connection():
        logging.warning("No internet connection")
        return {False: "No internet connection"}
    url = f"https://stc.mapotic.com/api/v1/poi/{turtle_id}/move/?page_size={positions_quantity}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        os.makedirs("../data/raw", exist_ok=True)
        with open(f"../data/raw/turtles{turtle_id}_positions_.json", "w") as f:
            json.dump(data, f)
        return {True: ""}

    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error occurred: {err}")
        return {False: f"HTTP error occurred: {err}"}
    except requests.Timeout as err:
        logging.error(f"Timeout error occurred: {err}")
        return {False: f"Timeout error occurred: {err}"}
    except requests.exceptions.RequestException as err:
        logging.error(f"Request error occurred: {err}")
        return {False: f"Request error occurred: {err}"}
    except ValueError:
        logging.error("Failed to decode JSON from response")
        return {False: "Failed to decode JSON from response"}
