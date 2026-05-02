import pandas as pd
from collections import defaultdict,Counter
import itertools
import numpy as np



def stream_four(tokenized_dataframe):
  unpacked_phrases = tokenized_dataframe.iloc[:,0].to_list()
  tokens = list(itertools.chain.from_iterable([phrase.split() for phrase in unpacked_phrases]))
  stemmer_model = n_gram_model(tokens,n=3)
  stemmer_model.create_model()
  return stemmer_model


def pad_sequences(func):
  def wrapper(*args,**kwargs):
    for arg in args:
      yield func(arg,**kwargs)
  return wrapper

@pad_sequences
def pad_sequence(sequence,**kwargs):
  n = kwargs['n']
  start_pad = ['<s>']*(n-1)
  end_pad = ['</s>']*(n-1)
  return start_pad + list(sequence.lower()) + end_pad


def get_sequence_counts(*args,**kwargs):
  n = kwargs['n']
  counts = defaultdict(Counter)
  for arg in args:
    for i in range(len(arg) - (n-1)):
      window = arg[i:i+n]
      counts[''.join(window[:-1])][window[-1]] += 1
  return counts


def convert_counts_to_probabilities(counts):
  counts_dataframe = pd.DataFrame(counts).T
  counts_dataframe = counts_dataframe.fillna(0)
  counts_dataframe += 0.01
  counts_dataframe = counts_dataframe / counts_dataframe.values.sum()
  return counts_dataframe


class n_gram_model:
  def __init__(self,sequences,n):
    self.sequences = pad_sequence(*sequences,n=n)
    self.n = n

  def create_model(self):
    counts = get_sequence_counts(*self.sequences,n=self.n)
    main_model = convert_counts_to_probabilities(counts)
    self.model = main_model

  def process_sequence(self,*args):
    for sequence in args:
      seq_len = len(sequence)
      padded_sequence = next(pad_sequence(sequence.lower(),n=self.n))
      block_probabilities = []
      for i in range(seq_len):
        window = padded_sequence[i:i+self.n]
        prefix,suffix = ''.join(window[:-1]),window[-1]
        if prefix not in self.model.index:
          block_probabilities.append(-np.log2(self.model.loc[:,suffix].sum()))
          continue
        joint_probability = self.model.loc[prefix,suffix]
        conditional_probability = joint_probability / self.model.loc[prefix].sum()
        block_probabilities.append(-np.log2(conditional_probability))
      yield block_probabilities


