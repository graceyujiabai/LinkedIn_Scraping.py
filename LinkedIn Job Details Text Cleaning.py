'''
Analyzing Job Descriptions Scraped from LinkedIn
'''

# import libraries
import pandas as pd
import numpy as np

# Text processing
import re
import string  ## do not import this as str!!!
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
job_data = pd.DataFrame(job_data.iloc[:, 1]).rename(columns={0: 'description'})

# split the data into columns
job_data_split = job_data['description'].str.split('\n', expand=True)

# print a concise summary of the split dataframe
print(job_data_split.info())

# from the data, it looks like columns 5:40 contain most of the useful data
# how can this step be less manual?
print(job_data_split.iloc[:, 5:41])
final_data = job_data_split.iloc[:, 5:41]

# look at our data
final_data.info()
final_data.isna().sum()

# final_data.drop_duplicates(inplace=True) # inplace: modify the dataset rather than creating a new one

# transform data into a list and append to original dataframe
# convert values to numpy arrays using .values and use .tolist() to convert the values to lists
final_data['to_list'] = final_data.values.tolist()

# transform a list into a string: ''.join() - the line below has issues/was not what you thought it was (all outputs
# look the same for each cell)
# final_data['to_string'] = ' '.join([str(x) for x in final_data['to_list']])

# combine useful columns into 1 column using .agg() (scales much better than .apply())
final_data['text_all'] = final_data[final_data.columns[0:]].astype(str).agg(' '.join, axis=1)

stop=None

# Combine all lists and do text cleaning: delete punctuation, stopwords, weird symbols, remove spacing, & transform
# everything into lower case tasks: extract bigrams. create wordclouds. single word frequency. additional tasks:
# group by company name; group by location (state); compare between DS and DA and BI and BA; analyze trends.

# # set stop_list to stopwords in English
# # from nltk import stopwords only imports the CorpusReader object. you cannot loop through the CorpusReader object.
# # must set(stopwords.words("english") to be able to loop through stopwords
stop_list = set(stopwords.words("english"))


def remove_punct(text):
    text = ''.join([word.lower() for word in text]) # make everything lowercase
    text = re.sub('\W+', ' ', text) # remove all special characters, spacing, and punctuation
    # text = re.sub('[^A-Za-z0-9]+', ' ', text)
    text = text.join([word for word in text if word not in stop_list])
    return text


final_data_all = final_data['text_all'].apply(lambda x: remove_punct(x))

print(final_data_all)
stop=None