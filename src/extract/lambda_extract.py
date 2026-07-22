import os
from .download import DownloadTse
from datetime import datetime
from zoneinfo import ZoneInfo

import boto3


def lambda_handler(event, context):
    """
    Lambda function to download TSE data and upload it to S3.
    event: {
        anos: lista 2024,
        folder: caminho para salvar no s3, padrão landing
        BUCKET_NAME: nome do bucket no s3

    }
    """

    s3 = boto3.client("s3")

    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))

    bucket_name = os.environ["BUCKET_NAME"]

    anos = event.get("anos", 2024)

    folder = event.get("folder", "landing")

    try:
        dados_tse = DownloadTse()

        files = dados_tse.download_ano(anos=[anos])

        for file in files:
            s3_key = f"{folder}/{agora:%Y/%m/%d}/{file['filename']}"

            s3.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=file["content"],
            )

        return {
            "statusCode": 200,
            "bucket": bucket_name,
            "totalFiles": len(files),
            "lastFileUploaded": s3_key,
        }
    except TypeError as e:
        return {
            "statusCode": 400,
            "error": str(e),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e),
        }
