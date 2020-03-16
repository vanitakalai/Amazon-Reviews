# check if spark exists and set properly
import findspark
findspark.init()
# import testing/logging modules
import logging
import pytest
# import spark modules
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SQLContext


def quiet_py4j():
    """ turn down spark logging for the test context """
    logger = logging.getLogger('py4j')
    logger.setLevel(logging.WARN)


@pytest.fixture(scope="session")
def spark_context(request):
    """ fixture for creating a spark context
    Args:
        request: pytest.FixtureRequest object
    """
    conf = (SparkConf().setMaster("local[2]").setAppName("pytest-pyspark-local-testing"))
    sc = SparkContext(conf=conf)
    request.addfinalizer(lambda: sc.stop())

    quiet_py4j()
    return sc

@pytest.fixture(scope="session")
def sql_context(spark_context):
    """  fixture for creating a sql context
    Args:
        spark_context: spark_context fixture
    Returns:
        SQLContext for tests
    """
    return SQLContext(spark_context)
