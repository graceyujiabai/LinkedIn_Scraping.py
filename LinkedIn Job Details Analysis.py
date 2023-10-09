'''
Analyzing Job Descriptions Scraped from LinkedIn
'''

# import libraries
import pandas as pd
import numpy as np

# Text processing
import re
import string ## do not import this as str!!!
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('punkt')
from nltk.tokenize import word_tokenize

# # Word cloud visualization
# from wordcloud import WordCloud, STOPWORDS
# from PIL import Image

# # Other visualization
# import matplotlib.pyplot as plt
# import plotly.express as px

data = []
for i in range(15):
    files = pd.read_csv(f"C:/Users/yujia/Desktop/pythonProject//LinkedIn Jobs{i}.csv")
    data.append(files['Job_Description'])

# Define our dataframe
job_data = pd.DataFrame(data)
# job_data = job_data[0]
print(job_data.head())

# Look at dataset
print(job_data.info())

# reset index and rename columns
job_data = job_data.reset_index().rename(columns={0: 'description', 'index': 'content'})

# pull the job description column out in the form of a dataframe
job_data = pd.DataFrame(job_data.iloc[:,1]).rename(columns={0: 'description'})

# split the data into columns
job_data_split = job_data['description'].str.split('\n', expand=True)

# print a concise summary of the split dataframe
print(job_data_split.info())

# from the data, it looks like columns 5:40 contain most of the useful data
# how can this step be less manual?
print(job_data_split.iloc[:,5:41])
final_data = job_data_split.iloc[:,5:41]


# look at our data
final_data.info()
final_data.isna().sum()

# drop duplicates - this step should not be done because we don't have a unique ID that identifies jobs. we may lose information.
# final_data.drop_duplicates(inplace=True) # inplace: modify the dataset rather than creating a new one

final_data.info()

# transform data into a list and append to original dataframe
# convert values to numpy arrays using .values and use .tolist() to convert the values to lists
final_data['to_list'] = final_data.values.tolist()
final_data['to_string'] = ''.join([str(x) for x in final_data['to_list']])

# combine all lists and do text cleaning
final_data_list = [item for item in final_data['to_list']]
final_data_string = ' '.join([str(x) for x in final_data_list])
stop=None

# delete punctuation
# delete stopwords
# delete weird symbols
# remove spacing
# transform everything into lower case
# tasks: extract bigrams. create wordclouds. single word frequency.
# additional tasks: group by company name. group by location (state). compare between DS and DA and BI and BA. analyze trends.

# def clean_text(text):
#     '''A function for cleaning text'''
#     text_1 = "".join([word.lower() for word in text if word not in string.punctuation])
#     text_2 = re.sub("[0-9]+", '', text_1)
#     text_3 = [word for word in text_2 if word not in stopwords]
#     return text_3

stop_list = set(stopwords.words("english"))
def remove_punct(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    # text = re.sub('[0–9]+', '', text)
    text = text.join([word for word in text if word not in stop_list])
    return text
final_data['punct'] = final_data['to_string'].apply(lambda x: remove_punct(x))

stop = None

final_data.head()
