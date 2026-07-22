import os
from .unzip import UnzipFiles


def lambda_handler(event, context):

    return {
        "statusCode": 200,
        "message": "Lambda function executed successfully.",
        "event": event,
    }
