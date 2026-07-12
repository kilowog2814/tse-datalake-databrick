import os
from extract.download import DownloadTse
from datetime import datetime
from zoneinfo import ZoneInfo

import boto3


def lambda_handler(event, context):
    """
    Espera receber:
    {
        "url": "https://site.com/arquivo.csv",
        "folder": "landing"
    }
    """
    s3 = boto3.client("s3")

    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))

    BUCKET_NAME = os.environ[
        "BUCKET_NAME"
    ]  ## Incluir no Environment Variables da Lambda.

    try:
        dados_tse = DownloadTse()

        files = dados_tse.download_ano([2024])

        folder = event.get("folder", "landing")

        for file in files:
            s3_key = f"{folder}/{agora:%Y/%m/%d}/{file['filename']}"

            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=s3_key,
                Body=file["content"],
            )

        return {
            "statusCode": 200,
            "bucket": BUCKET_NAME,
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
