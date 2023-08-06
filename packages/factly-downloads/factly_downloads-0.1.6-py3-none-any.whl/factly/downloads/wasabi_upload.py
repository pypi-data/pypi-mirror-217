import logging

import boto3

from .config import Settings


def validate_bucket_name(base_name: str) -> str:
    """Functionality to add prefix "stag" to Project base name while creating bucket

    Args:
        base_name (str): Project Name; example: "cricket"

    Returns:
        str: Project name with prefix stag-; example: "stag-cricket"
    """
    if not base_name.startswith("stag-"):
        base_name = f"stag-{base_name}"
    return base_name


settings = Settings()


def wasabi_upload(bucket_name: str, wasabi_path: str, local_file_path: str):
    """Functionality to upload a file to wasabi cloud, using file path

    Args:
        bucket_name (str): Bucket name to upload file to, usually project name, example: "cricket"
        wasabi_path (str): Location in wasabi to store. Recommended to use the same as local file path
        local_file_path (str): Local file path inside the Projects data directory, example: "cricket/2021/01/01/20210101-123456.csv"
    """
    # validate bucket name
    bucket_name = validate_bucket_name(bucket_name)

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        endpoint_url=settings.S3_HOST,
    )

    # Check if the bucket exists
    bucket_exists = False
    try:
        s3.head_bucket(Bucket=bucket_name)
        bucket_exists = True
    except Exception as e:
        logging.info(f"Bucket does not exist: {e}")

    # Create the bucket if it doesn't exist
    if not bucket_exists:
        logging.info(f"Creating bucket: {bucket_name}")
        s3.create_bucket(Bucket=bucket_name)
        logging.info(f"Bucket created: {bucket_name}")

    # Upload the file to the S3 bucket
    logging.info(f"Bucket name: {bucket_name}")
    logging.info(f"Uploading file: {local_file_path}")
    logging.info(f"Wasabi File path: {wasabi_path}")
    s3.upload_file(local_file_path, bucket_name, wasabi_path)
    logging.info("File uploaded successfully.")
