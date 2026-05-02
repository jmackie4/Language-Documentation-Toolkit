import pandas as pd
from collections import defaultdict,Counter
import os,re,itertools
from pathlib import Path

class WordCompendium:
  def __init__(self,tokenized_data,glossed_data,stemmer_model):
    self.tokenized_data = tokenized_data
    self.glossed_data = glossed_data
    self.stemmer_model = stemmer_model
    self.vocabulary = create_vocabulary(tokenized_data)
    self.compendium = None # Initialize compendium to None

  def fill_compendium(self):
    main_phrases = self.tokenized_data.iloc[:,0]
    word_concordances = {token:self.tokenized_data[main_phrases.str.contains(re.escape(token), regex=True, case=False)].index.to_list() for token in self.vocabulary}
    gloss_data = unpack_glossed_data(self.glossed_data)
    word_glosses = {token:gloss_data[token].most_common(3) for token in self.vocabulary}
    self.compendium = pd.DataFrame({'concordances':list(word_concordances.values()),
                         'gloss_data':list(word_glosses.values())},
                        index=list(word_glosses.keys()))

  def export_data(self):
    base_path = Path.home() / 'Desktop'
    export_folder_name = 'LDTK Created Resources'
    export_folder_path = os.path.join(str(base_path), export_folder_name)
    os.makedirs(export_folder_path, exist_ok=True)

    excel_file_path = os.path.join(export_folder_path, 'Corpus Resources.xlsx')

    with pd.ExcelWriter(excel_file_path) as writer:
      self.tokenized_data.to_excel(writer, sheet_name='Tokenized Data', index=True)
      self.glossed_data.to_frame(name='Glosses').to_excel(writer, sheet_name='Glossed Corpus', index=True)
      pd.DataFrame(list(self.vocabulary), columns=['Vocabulary']).to_excel(writer, sheet_name='Vocabulary', index=False)
      self.compendium.loc[:,'gloss_data'].to_excel(writer, sheet_name='Gloss Data', index=True)

    print(f"Exported data to {excel_file_path}")

  def get_concordances_for_words(self):
    if self.compendium is None:
      print("Compendium is not filled. Please run fill_compendium() first.")
      return

    print("\nEnter words separated by commas to get their concordances (type 'exit' to stop):\n")
    while True:
      user_input = input("Words: ")
      if user_input.lower() == 'exit' or not user_input.strip():
        print("Exiting concordance search.")
        break

      input_words = [word.strip().lower() for word in user_input.split(',')]
      valid_words = [word for word in input_words if word in self.vocabulary]

      if not valid_words:
        print("None of the entered words are in the vocabulary.")
        continue

      for word in valid_words:
        if word in self.compendium.index:
          print(f"\nConcordances for '{word}':")
          for _,row in self.tokenized_data.loc[self.compendium.loc[word,'concordances']].iterrows():
            print(f"{row.iloc[0]} ~~~~ {row.iloc[1]}")
        else:
          print(f"\nNo concordance data found for '{word}'.")
      print("\n")

  def get_glosses_for_words(self):
    if self.compendium is None:
      print("Compendium is not filled. Please run fill_compendium() first.")
      return

    print("\nEnter words separated by commas to get their glosses (type 'exit' to stop):\n")
    while True:
      user_input = input("Words: ")
      if user_input.lower() == 'exit' or not user_input.strip():
        print("Exiting gloss search.")
        break

      input_words = [word.strip().lower() for word in user_input.split(',')]
      valid_words = [word for word in input_words if word in self.vocabulary]

      if not valid_words:
        print("None of the entered words are in the vocabulary.")
        continue

      for word in valid_words:
        if word in self.compendium.index and 'gloss_data' in self.compendium.columns:
          print(f"\nGlosses for '{word}':")
          gloss_data = self.compendium.loc[word, 'gloss_data']
          if gloss_data:
            for gloss, count in gloss_data:
              print(f"  - {gloss} (count: {count})")
          else:
            print("  No gloss data available.")
        else:
          print(f"\nNo gloss data found for '{word}'.")
      print("\n")

  def use_stemmer(self):
      if self.compendium is None:
          print("Compendium is not filled. Please run fill_compendium() first.")
          return

      print("\nEnter words separated by commas to get their glosses (type 'exit' to stop):\n")
      while True:
          user_input = input("Words: ")
          if user_input.lower() == 'exit' or not user_input.strip():
              print("Exiting gloss search.")
              break

          input_words = [word.strip().lower() for word in user_input.split(',')]
          stemmer_results = self.stemmer_model.process_sequence(*input_words)
          for word,result in zip(input_words,stemmer_results):
              print(f"\nStemmer results for '{word}':")
              print(f"{result}")


def create_vocabulary(tokenized_df: pd.DataFrame):
  source_lang_series = tokenized_df.iloc[:, 0]
  converted_data = source_lang_series.to_list()
  split_data = [phrase.split() for phrase in converted_data]
  vocabulary = set(itertools.chain.from_iterable(split_data))
  return vocabulary


def unpack_glossed_data(glossed_data):
  glossed_data_list = list(itertools.chain.from_iterable(glossed_data.to_list()))
  main_gloss_data = defaultdict(Counter)
  for token,gloss in glossed_data_list:
    main_gloss_data[token][gloss] += 1
  return main_gloss_data