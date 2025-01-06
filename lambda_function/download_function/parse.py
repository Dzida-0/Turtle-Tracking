import json
import logging
from typing import Tuple


def parse_turtle_info(storage_handler) -> Tuple[dict, dict]:
    """
    Parse turtle information from a JSON file and update or insert records in the database.
    :param storage_handler: Instance of StorageHandler to interact with the storage system.
    :return: Dictionary mapping turtle IDs to their picture URLs.
    """
    ret_moves: dict = {}
    ret_picture: dict = {}
    try:
        # Load turtle info JSON from storage
        turtles_info_path = "json/turtles_info.json"
        content = storage_handler.load_file(turtles_info_path)
        data = json.loads(content)

        for turtle in data:
            turtle_id = turtle.get("id")
            motion = turtle.get("motion")
            if motion:
                moves_count = motion.get("active_moves")
                ret_moves[turtle_id] = moves_count

            image = turtle.get("image")
            if image:
                urls = image.get("urls", {})
                picture_url = urls.get("origin", None)
            else:
                picture_url = None

            ret_picture[turtle_id] = picture_url

    except FileNotFoundError:
        logging.error("Turtles info JSON file not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        return ret_moves, ret_picture
