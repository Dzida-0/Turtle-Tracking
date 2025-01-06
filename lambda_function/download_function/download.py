import logging
from .storage_handler import StorageHandler
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


def download_turtles_info(storage_handler: StorageHandler) -> Dict[bool, str]:
    url = "https://stc.mapotic.com/api/v1/poi/"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        storage_handler.save_file("json/turtles_info.json", response.text)
        return {True: ""}
    except Exception as err:
        logging.error(f"Failed to download turtle info: {err}")
        return {False: str(err)}


def download_turtles_positions(turtle_id: int, storage_handler: StorageHandler,
                               positions_quantity: Optional[int] = 10000, ) -> Dict[bool, str]:
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
        storage_handler.save_file(f'json/turtles{turtle_id}_positions.json', response.text)
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


def download_image(image_url: str, turtle_id: int, storage_handler: StorageHandler) -> Dict[bool, str]:
    """
    Download an image from a URL and save it as a PNG file in the configured folder.

    :param image_url: The URL of the image.
    :param turtle_id: The unique identifier of the turtle.
    :return: A dictionary indicating success (True/False) and a message (or empty string).
    """
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Ensure the request was successful

        storage_handler.save_photo(f'turtle_{turtle_id}.png', response)

        return {True: ""}
    except requests.exceptions.RequestException as e:
        return {False: f"Error downloading image: {e}"}
