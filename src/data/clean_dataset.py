import pyspark
from pyspark.sql import functions as F
from pyspark.sql.functions import isnan, when, count, col
from pyspark.sql.types import *
import logging

class Error(Exception):
    pass

class NullValueError(Error):
    def __init__(self):
        logging.error('Null values in dataset')

def check_null_values(data):
    no_error = True
    for column in data.columns:
        no_error = no_error & (data.where((col(column).isNull())|(col(column) == '')).count() == 0)
    return no_error

def check_types(data):
    return (data.select(col('review_body')).dtypes[0][1] == 'string') & \
                (data.select(col('star_rating')).dtypes[0][1] == 'int')

def check_values(data):
    rating_list = [i[0] for i in data.select(col('star_rating')).distinct().collect()]
    return sorted(rating_list) == [1, 2, 3, 4, 5]

def check_data(func, data, error):
    if func(data):
        pass
    else:
        raise error

def print_info(data):
    logging.info('There are {:,} reviews in this dataset'.format(data.count()))
    data.groupBy('star_rating').count().show()

def clean_data(data):

    logger = logging.getLogger(__name__)

    clean_data = data.dropna().select('review_headline', 'review_body', 'star_rating')\
                    .withColumn('star_rating',col('star_rating').cast(IntegerType()))\
                    .withColumn('reviews_headline',col('review_headline').cast(StringType()))\
                    .withColumn('review_body',col('review_body').cast(StringType()))\
                    .filter(col('star_rating').isin(1, 2, 3, 4, 5))\
                    .filter(col('review_body') != '')

    check_data(check_null_values, clean_data, NullValueError)
    logging.info("Null value check passed")
    check_data(check_types, clean_data, TypeError)
    logging.info("Type check passed")
    check_data(check_values, clean_data, ValueError)
    logging.info("Value check passed")
    print_info(clean_data)

    return clean_data
