import os
from pathlib import Path
from .utils import compendium, corpus_processor, gloss_stream, stemmer_stream


def create_corpus():
    desktop_path = Path.home() / 'Desktop'
    while True:
        user_path = input('Please give the name of the folder that has all your texts! ')
        if os.path.isdir(os.path.join(desktop_path,user_path)):
            return user_path
        else:
            print('The provided path is not a directory!')

def create_compendium():
    corpus_path = create_corpus()
    initial_df = corpus_processor.stream_one(corpus_path)
    tokenized_df = corpus_processor.stream_two(initial_df)
    glossed_df = gloss_stream.stream_three(tokenized_df)
    stemmer_model = stemmer_stream.stream_four(tokenized_df)
    current_compendium = compendium.WordCompendium(tokenized_df,glossed_df,stemmer_model)
    current_compendium.fill_compendium()
    return current_compendium


if __name__ == '__main__':
    compendium = create_compendium()
    options = {'get glosses': compendium.get_glosses_for_words,
               'get concordances': compendium.get_concordances_for_words,
               'use stemmer': compendium.use_stemmer,
               'export resources': compendium.export_data,
               }
    while True:
        for i,item in enumerate(options):
            print(f'{i}: {item}',end='\n')
        users_choice = input('Please enter what you want to do by typing out the name of the option: ')
        if users_choice.lower() in options :
            options[users_choice.lower()]()
        elif users_choice.lower() == 'exit':
            break
        else:
            print('Please enter a valid choice!')


