import os
from dotenv import load_dotenv
from download_data import download_turtles_info,download_turtles_positions,download_image, check_connection
from parsing_data import parse_turtle_info, parse_turtle_positions
import os
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def lambda_handler(event, context):
    event_log = []
    if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
        # production
        STORAGE = os.getenv('S3_BUCKET_NAME')
    else:
        # development
        STORAGE = os.getenv("LOCAL_STORAGE")

    # internet connection
    if not retry(check_connection, max_retries=3, delay=2):
        logger.error("Failed to establish connection after 3 attempts.")
        return {
            "statusCode": 500,
            "body": "Failed to establish connection"
        }

    # download
    if not retry(download_turtles_info(STORAGE), max_retries=3, delay=2):
        logger.error("Failed to establish connection after 3 attempts.")
        return {
            "statusCode": 500,
            "body": "Failed to establish connection"
        }



def retry(func, max_retries=3, delay=2, *args, **kwargs):
    """
    Retries a function up to `max_retries` times with a delay in seconds.
    """
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                return False

download_turtles_info()
dic = parse_turtle_info()
for i,j in dic.items():
    download_image(j,i)
    download_turtles_positions(i)
    parse_turtle_positions(i)