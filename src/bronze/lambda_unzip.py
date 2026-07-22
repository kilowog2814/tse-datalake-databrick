import os
from .unzip.UnzipFiles import zipfile


def lambda_handler(event, context):

    return {
        "statusCode": 200,
        "message": "Lambda function executed successfully.",
        "event": event,
    }
