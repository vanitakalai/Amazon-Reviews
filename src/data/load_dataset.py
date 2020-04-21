
# libraries to access variables
import os
from dotenv import load_dotenv, find_dotenv
# libraries for data manipulation
import pandas as pd
import numpy as np
# libraries for spark
import findspark
import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
#logging/error libraries
import logging

class Error(Exception):
    pass

class EnvironmentError(Error):
    def __init__(self, message):
        logging.error(message)

def check_env_variables():
    if [i in os.environ for i in ['SPARK_HOME', 'JAVA_HOME', 'HADOOP_HOME']] == [1, 1, 1]:
        logging.info('All environment variables present')
    else:
        raise EnvironmentError('Cannot find SPARK_HOME, JAVA_HOME or HADOOP_HOME in env variables')

def spark_initialize():
    try:
        findspark.init()
    except Exception as e:
        logging.error('Error with finding spark:' + e)

    conf = SparkConf().setAll([('spark.executor.memory', '4g'), ('spark.driver.memory', '4g'),
                            ('spark.app.name', 'amzn_reviews')])
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    return spark

def spark_s3_setup(spark, ACCESS_KEY, SECRET_KEY):
    spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", ACCESS_KEY)
    spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", SECRET_KEY)
    spark._jsc.hadoopConfiguration().set("fs.s3a.impl","org.apache.hadoop.fs.s3a.S3AFileSystem")
    spark._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider","org.apache.hadoop.fs.s3a.BasicAWSCredentialsProvider")

def load_data(spark, url, file_fmt, sep):
    try:
        data = spark.read.load(url, format=file_fmt, sep=sep, inferSchema="true", header="true")
        return data
    except Exception as e:
        logging.error(e)

def check_schema(data):
    true_schema = StructType([
        StructField('marketplace', StringType()),
        StructField('customer_id', IntegerType()),
        StructField('review_id', StringType()),
        StructField('product_id', StringType()),
        StructField('product_parent', IntegerType()),
        StructField('product_title', StringType()),
        StructField('product_category', StringType()),
        StructField('star_rating', IntegerType()),
        StructField('helpful_votes', IntegerType()),
        StructField('total_votes', IntegerType()),
        StructField('vine', StringType()),
        StructField('verified_purchase', StringType()),
        StructField('review_headline', StringType()),
        StructField('review_body', StringType()),
        StructField('review_date', StringType()),])
    assert (data.schema.fields == true_schema.fields), "Schema does not match amazon reviews schema"

def get_data():

    logger = logging.getLogger(__name__)

    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    SECRET_KEY = os.getenv("SECRET_KEY")
    ACCESS_KEY = os.getenv("ACCESS_KEY")

    # define bucket and key name to identify location where file is stored
    bucket = "amazon-reviews-pds/"
    key = "tsv/amazon_reviews_us_Electronics_v1_00.tsv.gz"

    check_env_variables()
    spark = spark_initialize()
    logging.info('Spark initialized')
    spark_s3_setup(spark, ACCESS_KEY, SECRET_KEY)
    logging.info('Spark S3 variables set')
    review_data = load_data(spark, "s3a://" + bucket + key, "csv", "\t")
    check_schema(review_data)
    logging.info('Dataset loaded successfully')

    return spark, review_data
