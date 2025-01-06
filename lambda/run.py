from dotenv import load_dotenv
from database_handler import DatabaseHandler
from storage_handler import StorageHandler
from download import download_turtles_info, download_turtles_positions, download_image, check_connection
from parse import parse_turtle_info
import os
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()


def lambda_handler(event, context):
    event_log = []
    if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
        # production
        storage_handler = StorageHandler(s3_bucket=os.getenv('S3_BUCKET_NAME'))
        db_handler = DatabaseHandler(
            db_uri={
                'host': os.getenv('RDS_HOST'),
                'user': os.getenv('RDS_USER'),
                'password': os.getenv('RDS_PASSWORD'),
                'database': os.getenv('RDS_DATABASE')
            },
            is_rds=True
        )
    else:
        # Local environment
        storage_handler = StorageHandler(local_path=os.getenv("LOCAL_STORAGE"))
        db_handler = DatabaseHandler(db_uri=os.getenv("LOCAL_SQLITE_URI"))

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
            "body": "Failed to download lambda"
        }

    db_handler.connect()

    # parse turtle info
    turtle_dict = parse_turtle_info(database_handler=db_handler, storage_handler=storage_handler)

    # download picture if not existing
    for turtle_id, url in turtle_dict.items():
        if url and not storage_handler.photo_exists(f'turtle_{turtle_id}.png'):
            if not retry(download_image, url, turtle_id, storage_handler, max_retries=3, delay=4):
                logger.error(f"Turtle {turtle_id} picture error url:{url}")

    # download turtle pos
    for turtle_id in turtle_dict.keys():
        if not retry(download_turtles_positions, turtle_id, storage_handler, max_retries=3, delay=4):
            db_handler.close()
            return {
                "statusCode": 500,
                "body": "Failed to download lambda"
            }
    # parse turtle pos

    db_handler.close()


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
