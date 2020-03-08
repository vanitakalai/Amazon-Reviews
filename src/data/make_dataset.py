# -*- coding: utf-8 -*-
import logging
import os.path
import boto3
import gzip
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from botocore.exceptions import ClientError

class Error(Exception):
    pass

class InputError(Error):
    def __init__(self, message, accepted_values):
        logging.error(message)
        logging.info(accepted_values)


def check_zipped(file_name):
    if file_name.endswith(('.gz')):
        return True
    elif file_name.endswith(('.tsv', '.csv')):
        return False
    else:
        raise InputError('Input file is incompatible with program',
                        'Accepted file types are .gz, .tsv and .csv')

def unzip(input_file_name, output_file_name):
    with gzip.open(input_file_name, 'rb') as in_file:
        with open(output_file_name, 'wb') as out_file:
            out_file.write(in_file.read())

def download_s3_file(access_key, secret_key, bucket, key, output_file_name):
    """Imports data from S3 bucket
    """
    s3 = boto3.client('s3', aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key)

    with open(output_file_name , 'wb') as write_file:
        try:
            s3.download_fileobj(bucket, key, write_file)
            logging.info('File downloaded succesfully at {}'.format(output_file_name))
        except ClientError as e:
            logging.error(e, exc_info=True)

def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('Downloading data from S3 bucket')

    SECRET_KEY = os.getenv("SECRET_KEY")
    ACCESS_KEY = os.getenv("ACCESS_KEY")

    # define bucket and key name to identify location where file is stored
    bucket = "amazon-reviews-pds"
    key = "tsv/amazon_reviews_us_Electronics_v1_00.tsv.gz"

    # define output destination for sample data file
    output_zipped_file = 'data/raw/amazon_review_data.gz'
    output_file = 'data/raw/amazon_review_data.tsv'

    download_s3_file(ACCESS_KEY, SECRET_KEY, bucket, key, output_zipped_file)

    if check_zipped(output_zipped_file):
        unzip(output_zipped_file, output_file)
        logging.info('File unzipped successfully at {}'.format(output_file))


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
