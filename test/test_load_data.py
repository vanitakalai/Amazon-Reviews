import pytest
import os
from pyspark.sql import Row
from pyspark.sql.types import *
from src.data.load_dataset import check_env_variables, check_schema, EnvironmentError


def test_env(monkeypatch):
    monkeypatch.delenv("SPARK_HOME", raising=False)

    with pytest.raises(EnvironmentError):
        check_env_variables()


pytestmark = pytest.mark.usefixtures("sql_context")
def test_schema(sql_context):
    mock_data = [{'a':'x', 'b':'y', 'c': 1}]
    mock_dataframe_1 = sql_context.createDataFrame(Row(**x) for x in mock_data)
    mock_schema_2 = StructType([
        StructField('marketplace', StringType()),
        StructField('customer_id', IntegerType()),
        StructField('review_id', StringType()),
        StructField('product_id', StringType()),
        StructField('product_parent', IntegerType()),
        StructField('product_tite', StringType()),
        StructField('product_category', StringType()),
        StructField('star_rating', IntegerType()),
        StructField('helpful_votes', IntegerType()),
        StructField('total_votes', IntegerType()),
        StructField('vine', StringType()),
        StructField('verified_purchase', StringType()),
        StructField('review_headline', StringType()),
        StructField('review_body', StringType()),
        StructField('review_date', StringType()),])
    mock_dataframe_2 = sql_context.createDataFrame([], mock_schema_2)
    mock_schema_3 = StructType([
        StructField('marketplace', IntegerType()),
        StructField('customer_id', IntegerType()),
        StructField('review_id', StringType()),
        StructField('product_id', StringType()),
        StructField('product_parent', IntegerType()),
        StructField('product_tite', StringType()),
        StructField('product_category', StringType()),
        StructField('star_rating', IntegerType()),
        StructField('helpful_votes', IntegerType()),
        StructField('total_votes', IntegerType()),
        StructField('vine', StringType()),
        StructField('verified_purchase', StringType()),
        StructField('review_headline', StringType()),
        StructField('review_body', StringType()),
        StructField('review_date', StringType()),])
    mock_dataframe_3 = sql_context.createDataFrame([], mock_schema_3)

    with pytest.raises(AssertionError):
        check_schema(mock_dataframe_1)
        check_schema(mock_dataframe_2)
        check_schema(mock_dataframe_3)


if __name__ == '__main__':
    pytest.main()
