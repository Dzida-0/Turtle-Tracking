import json
import os
import logging
from dotenv import load_dotenv
import time
from .download import download_turtles_info, check_connection, download_image, download_turtles_positions
from .storage_handler import StorageHandler
from .parse import parse_turtle_info

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()


def lambda_handler(event, context):
    if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
        # production
        storage_handler = StorageHandler(s3_bucket=os.getenv('S3_BUCKET_NAME'))
    else:
        # Local environment
        storage_handler = StorageHandler(local_path=os.getenv("LOCAL_STORAGE"))

    # internet connection
    if not retry(check_connection, max_retries=3, delay=2):
        return {
            "statusCode": 500,
            "body": "Failed to establish connection"
        }

    # download turtle info
    if not retry(download_turtles_info, storage_handler, max_retries=3, delay=4):
        return {
            "statusCode": 500,
            "body": "Failed to download turtle_info"
        }

    # parse info
    moves, picture = parse_turtle_info(storage_handler)

    # download_function photos
    to_remove = []
    for turtle_id, url in picture.items():
        if url:
            if not storage_handler.file_exists(f"photos/turtle_{turtle_id}.png"):
                if not retry(download_image, url, turtle_id, storage_handler, max_retries=3, delay=4):
                    logger.error(f"Turtle {turtle_id} picture error url:{url}")
                else:
                    to_remove.append(turtle_id)
            else:
                to_remove.append(turtle_id)
    for i in to_remove:
        picture.pop(i)
    storage_handler.save_file("json/config_photos.json", json.dumps(picture))

    # download positions
    if storage_handler.file_exists("json/config_moves.json"):
        old_moves = json.loads(storage_handler.load_file("json/config_moves.json"))
        for turtle_id, moves_count in moves.items():
            if int(old_moves[str(turtle_id)]) < int(moves_count):
                if not retry(download_turtles_positions, turtle_id, storage_handler, int(moves_count) - int(old_moves[str(turtle_id)]),
                             max_retries=3, delay=4):
                    return {
                        "statusCode": 500,
                        "body": "Failed to download lambda_old"
                    }
        storage_handler.save_file("json/config_moves.json", json.dumps(moves))
    else:
        for turtle_id in moves.keys():
            if not retry(download_turtles_positions, turtle_id, storage_handler, max_retries=3, delay=4):
                return {
                    "statusCode": 500,
                    "body": "Failed to download lambda_old"
                }
        storage_handler.save_file("json/config_moves.json", json.dumps(moves))


def retry(func, *args, max_retries=3, delay=2, **kwargs):
    """
    Retries a function up to `max_retries` times with a delay in seconds.
    """
    for attempt in range(max_retries):
        result = func(*args, **kwargs)
        if result.get(True) == '':
            return True
        logger.warning(f"Attempt {attempt + 1} failed. {result.get(False)}")
        time.sleep(delay)
    return False
