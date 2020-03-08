import pytest
import gzip
import mock
from src.data.make_dataset import check_zipped, unzip, InputError

def test_check_zipped():
    assert(check_zipped('abcd.gz')) == True
    assert(check_zipped('abcd.csv')) == False
    with pytest.raises(InputError):
        check_zipped('abcd.txt')


if __name__ == '__main__':
    test_check_zipped()
