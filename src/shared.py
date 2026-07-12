import boto3
import os
from loguru import logger


class Shared:
    """
    Cria os objetos para os outros scripts

    """

    def __init__(self) -> None:
        self.bucket = os.getenv("BUCKET_NAME")
        self.region = os.getenv("AWS_REGION", "us-east-1")

        self.s3 = boto3.client("s3", region_name=self.region)

        self.landing_path = "landing"
        self.bronze_path = "bronze"
        self.data_path = "data"
        self.logger = logger
