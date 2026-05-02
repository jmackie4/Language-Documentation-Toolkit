import os,spacy,itertools,nltk
import pandas as pd
import numpy as np
from nltk.tokenize import RegexpTokenizer
from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import TfidfTransformer
from pathlib import Path

def stream_two(initial_dataframe):
  lowercased_df = lower_strings(initial_dataframe)
  tokenized_df = tokenize_dataframe_column(lowercased_df)
  return tokenized_df


def stream_one(folder_name):
  loaded_texts = load_texts(folder_name)
  df = create_dataframe(loaded_texts)
  return df


def load_texts(folder_name):
  my_drive_path = Path.home() / 'desktop'
  root_folder_path = my_drive_path + '/' + folder_name
  for filename in os.listdir(root_folder_path):
    with open(os.path.join(root_folder_path,filename),'r') as file:
      all_lines = file.readlines()
      source_lang_lines = [line for i,line in enumerate(all_lines) if i % 2 == 0]
      target_lang_lines = [line for i,line in enumerate(all_lines) if i % 2 != 0]
      yield {filename[:-4]:zip(source_lang_lines,target_lang_lines)}


def create_dataframe(loaded_texts):
  column_one,column_two = [],[]
  index_tuples = []
  for text in loaded_texts:
    title = list(text.keys())[0]
    contents = list(text[title])
    text_length = [i for i,_ in enumerate(contents)]
    index_tuples.extend(list(zip(itertools.repeat(title),text_length)))
    column_one.extend([line[0] for line in contents])
    column_two.extend([line[1] for line in contents])

  multi_index = pd.MultiIndex.from_tuples(index_tuples)
  dataframe_columns = {'source_lang':column_one,'target_lang':column_two}
  df = pd.DataFrame(dataframe_columns,index=multi_index)
  return df

def lower_strings(input_dataframe):
  lowercased_dataframe = input_dataframe.map(lambda x: x.lower())
  return lowercased_dataframe

def tokenize_dataframe_column(input_dataframe,regex_pattern=r'''\w+(?:'\w+)?(?:|[--‐]+)?\w+(?:'\w+)?'''):
  nlp = spacy.load('en_core_web_sm')
  input_copy = input_dataframe.copy()
  tokenizer = RegexpTokenizer(regex_pattern)
  input_copy['source_lang'] = input_copy['source_lang'].apply(lambda x: ' '.join(tokenizer.tokenize(x)))
  input_copy['target_lang'] = input_copy['target_lang'].apply(lambda x: ' '.join([token.text.lower() for token in nlp(x) if token.is_punct is False]))
  return input_copy


