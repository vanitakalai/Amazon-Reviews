import pyspark
from pyspark.sql import functions as F
from pyspark.sql.functions import isnan, when, count, col, regexp_replace, trim, lower
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
    return (data.select(col('clean_body')).dtypes[0][1] == 'string') & \
                ('int' in data.select(col('star_rating')).dtypes[0][1])

def check_values(data):
    rating_list = [i[0] for i in data.select(col('star_rating')).distinct().collect()]
    return sorted(rating_list) == [1, 2, 3, 4, 5]

def check_data(func, data, error):
    if func(data):
        pass
    else:
        raise error

def print_info(data):
    logging.info('Printing info about data:')
    logging.info('There are {:,} reviews in this dataset'.format(data.count()))
    data.printSchema()
    data.groupBy('star_rating').count().show()

def remove_punctuation(column):
    column = regexp_replace(column, "<br />", " ")
    column = regexp_replace(column, "&#34;", "")
    return trim(lower(regexp_replace(column, '[^\sa-zA-Z0-9]', '')))

def write_to_csv(data, filepath):
    try:
        data.write.format("com.databricks.spark.csv").save(filepath)
        logging.info('Completed writing to file at:' + filepath)
    except Exception as e:
        logging.error('Need to have spark-csv package.' + e)


def clean_data(data):

    logger = logging.getLogger(__name__)
    filepath = 'data/processed/clean_reviews'

    clean_data = data.withColumn('clean_body', remove_punctuation(col('review_body')))\
                    .select('clean_body', 'star_rating')\
                    .dropna()\
                    .withColumn('star_rating',col('star_rating').cast(IntegerType()))\
                    .withColumn('clean_body',col('clean_body').cast(StringType()))\
                    .filter(col('star_rating').isin(1, 2, 3, 4, 5))\
                    .filter(col('clean_body') != '')

    check_data(check_null_values, clean_data, NullValueError)
    logging.info("Null value check passed")
    check_data(check_types, clean_data, TypeError)
    logging.info("Type check passed")
    check_data(check_values, clean_data, ValueError)
    logging.info("Value check passed")
    print_info(clean_data)

    # requires installation of package from databricks
    write_to_csv(clean_data, filepath)

    return filepath
