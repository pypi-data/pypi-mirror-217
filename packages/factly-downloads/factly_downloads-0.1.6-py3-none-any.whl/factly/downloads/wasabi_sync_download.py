import datetime
import logging
import os
from pathlib import Path

import boto3

from .config import Settings

settings = Settings()


def sync_files(project_bucket_path, remote_directory_name, local_file_list, local_path):
    """
    Summary: it creates a replica in local by checking local files and wasabi files

    Args:
        project_bucket_path (s3 bucket object): _description_
        remote_directory_name (string): it describes the wasabi file path
        local_file_list (List): it is a list of files in local machine
    """
    # filtering the objects based on wasabi path
    if len(list(project_bucket_path.objects.filter(Prefix=remote_directory_name))) != 0:
        for obj in project_bucket_path.objects.filter(Prefix=remote_directory_name):
            # check if wasabi file exist in local or not and which is latest
            exists_local = (
                str(obj.key).split(f"{remote_directory_name}")[-1] in local_file_list
            )
            lastest_on_local = False
            if exists_local:
                lastest_on_local = (
                    datetime.datetime.fromtimestamp(
                        os.stat(Path(local_path / str(obj.key))).st_mtime
                    )
                    > obj.last_modified
                )
                logging.info(" - File exist in local and but has new version on s3")
                if lastest_on_local:
                    logging.info(" - File exist in local and is latest")
            else:
                if obj.size != 0:
                    logging.info(" - File does not exist in local")
                    output_file = get_directory(
                        obj.key, local_path, remote_directory_name
                    )
                    logging.info(f" Downloading file {obj.key} to {str(output_file)}")
                    project_bucket_path.download_file(Filename=output_file, Key=obj.key)
                else:
                    logging.info("--skipping file as it is of size zero")
    else:
        logging.info(" - Please check wasabi_path for existence")
    return


def get_directory(file_path, local_path, remote_directory_name):
    """
    Summary: This function takes string of file wasabi file path and generates folder structure in local machine if needed and produces local file path

    Args:
        file_path (String): it is the wasabi file path

    Returns:
        output_file (String): it is the output file path
    """
    if len(file_path.split(f"{remote_directory_name}")[-1].strip("/").split("/")) > 1:
        local_path = (
            local_path
            + "/"
            + "/".join(
                file_path.split(f"{remote_directory_name}")[-1]
                .strip("/")
                .split("/")[:-1]
            )
        )
    output_folder = Path(local_path).resolve()
    output_folder.mkdir(exist_ok=True, parents=True)
    output_file = str(output_folder) + f"/{file_path.split('/')[-1]}"
    return output_file


def wasabi_sync_download(bucket_name, wasabi_path, local_path):
    """
    Summary: this function replicate the wasabi files in particular path to the local by comparing local and remote

    Args:
        bucket_name (String): wasabi bucket name
        wasabi_path (String): wasabi path
        local_path (String): local folder path
    """
    # handling improper input
    wasabi_path = wasabi_path.strip("/")
    local_path = local_path.strip("/")
    local_path = "/" + local_path

    # starting wasabi session
    session = boto3.Session(
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION,
    )
    s3 = session.resource(
        "s3", endpoint_url=settings.S3_HOST, region_name=settings.S3_REGION
    )
    project_bucket_path = s3.Bucket(bucket_name)
    remote_directory_name = wasabi_path
    # checking local files
    local_path_file = list(Path(local_path).glob("**/*.*"))
    # creating file list
    local_file_list = [str(i).split(f"{local_path}")[-1] for i in local_path_file]
    sync_files(project_bucket_path, remote_directory_name, local_file_list, local_path)
    return True
