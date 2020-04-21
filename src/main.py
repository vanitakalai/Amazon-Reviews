from data.load_dataset import get_data
from data.clean_dataset import clean_data
import logging
import os.path


def main():

    spark, data = get_data()
    filepath = clean_data(data)
    spark.stop()


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
