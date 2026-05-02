import pandas as pd
from collections import Counter
import itertools
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import TfidfTransformer


#The main stream that processes the dataframe and returns a generator where each text is glossed
def gloss_dataframe(tokenized_dataframe):
  aligner_model = entropy_glosser()
  aligner_model.fit(tokenized_dataframe)
  for _,row in tokenized_dataframe.iterrows():
    yield aligner_model.predict(row.iloc[0],row.iloc[1])

def stream_three(tokenized_dataframe):
  gloss_generator = gloss_dataframe(tokenized_dataframe)
  main_index = tokenized_dataframe.index
  return pd.Series(gloss_generator,index=main_index)

#Main Class Objects For Glossing Stream
class BaseGlosser(BaseEstimator):
    def __init__(self):
        pass

    def fit(self,X,y=None):
        self.model = pd.DataFrame(X)
        return self

    def predict(self, source_text: str, target_text: str):
        source_tokens_counter = Counter([token for token in source_text.split() if token in self.model.index])
        target_tokens_counter = Counter([token for token in target_text.split() if token in self.model.columns])
        return self.predict_recursively(source_tokens_counter, target_tokens_counter)

    def predict_recursively(self,X:Counter,y:Counter):
        x_list = [key for key,value in X.items() if value > 0]
        y_list = [key for key,value in y.items() if value > 0]
        results = []
        if x_list == [] or y_list == []:
            if y_list == []:
                return results + [(item,'no gloss') for item in x_list if x_list != []]
            elif x_list == []:
                return results + [('no source',item) for item in y_list if y_list != []]


        elif len(x_list) == 1:
            if not y_list:
                return results + [(x_list[0], 'no gloss')]
            return results + [(x_list[0],self.model.loc[x_list[0],y_list].idxmax())]

        elif len(x_list) > 1:
            if not y_list:
                return results + [(item, 'no gloss') for item in x_list]
            best_target = self.model.loc[x_list[0],y_list].idxmax()
            results.append((x_list[0], best_target))
            X[x_list[0]] -= 1
            y[best_target] -= 1
            return results + self.predict_recursively(X,y)


class tfidf_glosser(BaseGlosser):
    def __init__(self):
        super().__init__()

    def fit(self,X:pd.DataFrame,y=None):
        frequency_table = create_frequency_table(X)
        vectorizer = TfidfTransformer()
        tfidf_matrix = vectorizer.fit_transform(frequency_table)
        self.model = pd.DataFrame.sparse.from_spmatrix(tfidf_matrix,index=frequency_table.index, columns=vectorizer.get_feature_names_out())
        return self


class entropy_glosser(BaseGlosser):
    def __init__(self):
        super().__init__()

    def fit(self, X:pd.DataFrame, y=None):
        self.model = transform_dataframe_to_entropy_table(X)
        return self

    def predict_recursively(self, X: Counter, y: Counter):
        x_list = [key for key, value in X.items() if value > 0]
        y_list = [key for key, value in y.items() if value > 0]
        results = []
        if x_list == [] or y_list == []:
            if y_list == []:
                return results + [(item, 'no gloss') for item in x_list if x_list != []]
            elif x_list == []:
                return results + [('no source', item) for item in y_list if y_list != []]

        elif len(x_list) == 1:
            if not y_list:
                return results + [(x_list[0], 'no gloss')]
            return results + [(x_list[0], self.model.loc[x_list[0], y_list].idxmin())]

        elif len(x_list) > 1:
            if not y_list:
                return results + [(item, 'no gloss') for item in x_list]

            y_list_with_entropy = y_list + ['Entropy']
            valid_columns = [col for col in y_list_with_entropy if col in self.model.columns]

            if not valid_columns or len(valid_columns) == 1 and 'Entropy' in valid_columns:
                return results + [(item, 'no gloss') for item in x_list]

            token_glosses = self.model.loc[x_list, valid_columns]

            if 'Entropy' in token_glosses.columns:
                token_glosses = token_glosses.sort_values(by=['Entropy'])
                token_glosses = token_glosses.drop('Entropy',axis=1)

            if token_glosses.empty or token_glosses.columns.empty:
                return results + [(item, 'no gloss') for item in x_list]

            best_source_token = token_glosses.index[0]
            best_glossed_token = token_glosses.iloc[0].idxmin()

            results.append((best_source_token, best_glossed_token))
            X[best_source_token] -= 1
            y[best_glossed_token] -= 1
            return results + self.predict_recursively(X, y)


#Helper functions for glossing stream
def transform_dataframe_to_entropy_table(X:pd.DataFrame):
    frequency_table = create_frequency_table(X)
    probability_table = create_probability_table(frequency_table)
    return create_entropy_table(probability_table)

def create_entropy_table(probability_table:pd.DataFrame):
    entropy_table =  np.log2(probability_table) * -1
    entropy_vector = (entropy_table * probability_table).sum(axis=1)
    entropy_table['Entropy'] = entropy_vector
    return entropy_table

def create_probability_table(freq_table:pd.DataFrame):
    return freq_table.div(freq_table.sum(axis=1),axis=0)

def create_frequency_table(X:pd.DataFrame):
    unpacked_dataframe = X.to_numpy().T.tolist()
    gloss_counter = create_gloss_counter(unpacked_dataframe)
    df_index = sorted(list(set([key[0] for key in gloss_counter.keys()])))
    df_columns = sorted(list(set([key[1] for key in gloss_counter.keys()])))
    frequency_dataframe = pd.DataFrame(1, index=df_index, columns=df_columns)
    for key, value in gloss_counter.items():
        frequency_dataframe.loc[key[0], key[1]] += value
    return frequency_dataframe

def split_items(list_of_strings):
  for string in list_of_strings:
    yield set(string.split())

def create_cartesian_products(list_of_strings):
  generator_a = split_items(list_of_strings[0])
  generator_b = split_items(list_of_strings[1])
  for list_a,list_b in zip(generator_a,generator_b):
    yield list(itertools.product(list_a,list_b))

def create_gloss_counter(list_of_strings):
  cartesian_products = create_cartesian_products(list_of_strings)
  return Counter(itertools.chain.from_iterable(cartesian_products))


