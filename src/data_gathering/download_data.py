import json
import logging
import os
from typing import Optional

import requests


def check_connection() -> bool:
    """
    Check if there is an internet connection by pinging Google's website.
    :return: True if successfully connected, False otherwise.
    """
    try:
        response = requests.get("https://www.google.com", timeout=3)
        if response.status_code == 200:
            return True
        return False
    except requests.ConnectionError as err:
        logging.error(f"Connection error occurred: {err}")
    except requests.Timeout as err:
        logging.error(f"Timeout error occurred: {err}")
    return False


def download_turtles_info() -> bool:
    """
    Download all information about turtles (name, species, ect.)
    :return: True if successfully downloaded, False otherwise.
    """
    if not check_connection():
        logging.warning("No internet connection")
        return False
    url = "https://stc.mapotic.com/api/v1/poi/"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        os.makedirs("../data/raw", exist_ok=True)
        with open("../data/raw/turtles_info.json", "w") as f:
            json.dump(data, f)
        return True

    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Request error occurred: {err}")
    except ValueError:
        logging.error("Failed to decode JSON from response")
    return False


def download_turtles_positions(turtle_id: int, positions_quantity: Optional[int] = 10000) -> bool:
    """
    Download all position and movement related information for given turtle
    :param turtle_id: ID number of turtle
    :param positions_quantity: Amount of last positions to be downloaded
    :return: True if successfully downloaded, False otherwise.
    """
    if not check_connection():
        logging.warning("No internet connection")
        return False
    url = f"https://stc.mapotic.com/api/v1/poi/{turtle_id}/move/?page_size={positions_quantity}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        os.makedirs("../data/raw", exist_ok=True)
        with open(f"../data/raw/turtles{turtle_id}_positions_.json", "w") as f:
            json.dump(data, f)
        return True

    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Request error occurred: {err}")
    except ValueError:
        logging.error("Failed to decode JSON from response")
    return False
