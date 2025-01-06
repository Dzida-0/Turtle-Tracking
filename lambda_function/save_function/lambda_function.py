import logging
import os
from .database_handler import DatabaseHandler
from .storage_handler import StorageHandler
from .parse import parse_turtle_info,parse_turtle_positions

def lambda_handler(event, context):
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

    db_handler.connect()
    # parse turtle info
    turtles = parse_turtle_info(database_handler=db_handler, storage_handler=storage_handler)
    # parse turtle position
    for turtle_id in turtles:
        parse_turtle_positions(turtle_id,db_handler,storage_handler)
    db_handler.close()
