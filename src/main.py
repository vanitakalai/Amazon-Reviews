from data.load_dataset import get_data
from data.clean_dataset import clean_data
import logging
#import clean_dataset


def main():

    data = get_data()
    cleaned_data = clean_data(data)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
