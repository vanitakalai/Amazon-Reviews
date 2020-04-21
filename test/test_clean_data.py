import pytest
from src.data.clean_dataset import check_null_values, check_values, check_types, remove_punctuation
from pyspark.sql.types import StringType, StructType, StructField
from pyspark.sql.functions import col


pytestmark = pytest.mark.usefixtures("sql_context")

@pytest.fixture(scope='module')
def data_gen():
    def gen_func(sql_context, id = True):
        labels = ['star_rating', 'clean_body']
        if id:
            return sql_context.createDataFrame(
                [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five')], labels)
        else:
            return sql_context.createDataFrame(
                [(1, 1), (6, None), (7, 3), (4, 4), (5, 5)], labels)
    return gen_func

@pytest.fixture(scope='module')
def string_gen():
    def gen_strings_df(sql_context, strings):
        return  sql_context.createDataFrame([[i] for i in strings],
                        StructType([StructField("strings", StringType(), True)]))
    return gen_strings_df

strings = ['This was good. The product was GREAT!',
                'The product was bad, and late.<br />As they said &#34;NEver trust AMZN&#34;']
transformed_strings = ['this was good the product was great',
                'the product was bad and late as they said never trust amzn']


def test_check_null_values(data_gen, sql_context):
    assert check_null_values(data_gen(sql_context))
    assert check_null_values(data_gen(sql_context, False)) == False

def test_check_values(data_gen, sql_context):
    assert check_values(data_gen(sql_context))
    assert check_values(data_gen(sql_context, False)) == False

def test_check_types(data_gen, sql_context):
    assert check_types(data_gen(sql_context))
    assert check_types(data_gen(sql_context, False))== False

def test_remove_punctuation(string_gen, sql_context):
    string_df = string_gen(sql_context, strings)
    transformed_string_df = string_gen(sql_context, transformed_strings)
    assert string_df.select(remove_punctuation(col('strings'))).subtract(transformed_string_df).count() == 0


if __name__ == '__main__':
    pytest.main()
