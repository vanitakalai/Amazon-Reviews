## Project Proposal: Amazon Reviews

### Problem Statement

<b>People are increasingly using social media to disseminate their views on products they have purchased and companies do not have a structured way of extracting this data and analysing it for sentiment. Most companies still rely on reviews being written to them or posted to their page to understand the impact of their product. This tends to be a small sample size and there are now many labelled datasets which can be used to train an in-house sentiment analysis tool for unlabelled data. In this case, we will be creating a tool for a client selling electronic products using the Amazon electronics reviews dataset. The client will be able to use this tool to analyse the sentiment of unlabelled textual data about their products and hence, be able to make better decisions about their product.

### Data Extraction

<b>The project is based on the set of reviews provided by Amazon through their S3 service. More information on the dataset can be found at https://s3.amazonaws.com/amazon-reviews-pds/tsv/index.txt. The projects aims to use this labelled dataset to develop a tool that can perform textual sentimental analysis for other unlabelled data e.g. on twitter and other social media.


```python
import os.path
import boto3
import pandas as pd
import logging
from dotenv import load_dotenv
from botocore.exceptions import ClientError
```

<b>The dataset can be downloaded into a csv file using the [`boto3`](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) module. The function `download_s3_file` will do this for you. Here, I have downloaded a very small sample dataset as an example. 


```python
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_KEY = os.getenv("ACCESS_KEY")
```


```python
def download_s3_file(access_key, secret_key, bucket, key, output_folder_name, output_file_name):
    
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    
    with open(output_folder_name + output_file_name , 'wb') as write_file:
        try:
            s3.download_fileobj(bucket, key, write_file)
            logging.info('File downloaded succesfully at {}'.format(folder_name + file_name))    
        except ClientError:
            logging.error("Invalid credentials", exc_info=True)
```


```python
# define bucket and key name to identify location where file is stored
bucket = "amazon-reviews-pds"
key = "tsv/sample_us.tsv"
# define output destination for sample data file
folder_name = os.path.abspath('..') + '/data/external'
file_name = '/sample_data.csv'
```


```python
download_s3_file(ACCESS_KEY, SECRET_KEY, bucket, key, folder_name, file_name)
sample_data_df = pd.read_csv(folder_name + file_name, sep='\t')
```


```python
sample_data_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>marketplace</th>
      <th>customer_id</th>
      <th>review_id</th>
      <th>product_id</th>
      <th>product_parent</th>
      <th>product_title</th>
      <th>product_category</th>
      <th>star_rating</th>
      <th>helpful_votes</th>
      <th>total_votes</th>
      <th>vine</th>
      <th>verified_purchase</th>
      <th>review_headline</th>
      <th>review_body</th>
      <th>review_date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>US</td>
      <td>18778586</td>
      <td>RDIJS7QYB6XNR</td>
      <td>B00EDBY7X8</td>
      <td>122952789</td>
      <td>Monopoly Junior Board Game</td>
      <td>Toys</td>
      <td>5</td>
      <td>0</td>
      <td>0</td>
      <td>N</td>
      <td>Y</td>
      <td>Five Stars</td>
      <td>Excellent!!!</td>
      <td>2015-08-31</td>
    </tr>
    <tr>
      <th>1</th>
      <td>US</td>
      <td>24769659</td>
      <td>R36ED1U38IELG8</td>
      <td>B00D7JFOPC</td>
      <td>952062646</td>
      <td>56 Pieces of Wooden Train Track Compatible wit...</td>
      <td>Toys</td>
      <td>5</td>
      <td>0</td>
      <td>0</td>
      <td>N</td>
      <td>Y</td>
      <td>Good quality track at excellent price</td>
      <td>Great quality wooden track (better than some o...</td>
      <td>2015-08-31</td>
    </tr>
    <tr>
      <th>2</th>
      <td>US</td>
      <td>44331596</td>
      <td>R1UE3RPRGCOLD</td>
      <td>B002LHA74O</td>
      <td>818126353</td>
      <td>Super Jumbo Playing Cards by S&amp;S Worldwide</td>
      <td>Toys</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>N</td>
      <td>Y</td>
      <td>Two Stars</td>
      <td>Cards are not as big as pictured.</td>
      <td>2015-08-31</td>
    </tr>
    <tr>
      <th>3</th>
      <td>US</td>
      <td>23310293</td>
      <td>R298788GS6I901</td>
      <td>B00ARPLCGY</td>
      <td>261944918</td>
      <td>Barbie Doll and Fashions Barbie Gift Set</td>
      <td>Toys</td>
      <td>5</td>
      <td>0</td>
      <td>0</td>
      <td>N</td>
      <td>Y</td>
      <td>my daughter loved it and i liked the price and...</td>
      <td>my daughter loved it and i liked the price and...</td>
      <td>2015-08-31</td>
    </tr>
    <tr>
      <th>4</th>
      <td>US</td>
      <td>38745832</td>
      <td>RNX4EXOBBPN5</td>
      <td>B00UZOPOFW</td>
      <td>717410439</td>
      <td>Emazing Lights eLite Flow Glow Sticks - Spinni...</td>
      <td>Toys</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>N</td>
      <td>Y</td>
      <td>DONT BUY THESE!</td>
      <td>Do not buy these! They break very fast I spun ...</td>
      <td>2015-08-31</td>
    </tr>
  </tbody>
</table>
</div>




```python
sample_data_df.columns
```




    Index(['marketplace', 'customer_id', 'review_id', 'product_id',
           'product_parent', 'product_title', 'product_category', 'star_rating',
           'helpful_votes', 'total_votes', 'vine', 'verified_purchase',
           'review_headline', 'review_body', 'review_date'],
          dtype='object')



<b> The most important columns will be review body and star rating. Our target will be the star ratings and we will train our machine learning algorithm on the review body. We will use some NLP techniques to tokenize the text data, followed by using different types of neural networks to train the data on. It is likely that we will also depend on existing models to build our base models. The deliverables will be the code posted on github, along with a report and presentation summarizing the process and outcome.