# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 14:21:35 2023

@author: Daniel
"""
import pandas as pd
import numpy as np

WEIGHTS_RESULTS_CSV = "weights.csv"

PRONOUNS_FILE = "Pronombres/pronombres.txt"

VERBS_PREFIX = "Verbos/"
VERBS_FORMS_FILE = f"{VERBS_PREFIX}formas_verbos.txt"

KEYWORDS_PREFIX = "PalabrasClave/"
KEYWORDS_FORMS_FILE = f"{KEYWORDS_PREFIX}formas_palabras_clave.txt"

ELON_ANSWERS = 

def main():
    weights_df = load_dataframe()
    pronouns_dict, verbs_dict, keywords_dict, elon_dict = load_dictionaries()
    
    dimensions = weights_df.columns
    n_dimensions = len(dimensions)
    while True:
        question = get_question()
        scores_array = get_question_scores(question, 
                                           weights_df, 
                                           n_dimensions,
                                           pronouns_dict,
                                           verbs_dict,
                                           keywords_dict)
        show_answers(scores_array, dimensions)
        
        
def get_question():
    question = input("Por favor, introduce una pregunta acerca de Elon Musk o Steve Jobs:")
    question = clear_question(question)
    return question


def get_question_scores(question, 
                        weights_df,
                        n_dimensions, 
                        pronouns_dict,
                        verbs_dict,
                        keywords_dict):
    
    scores = np.zeros(n_dimensions)
    for word in question.split(" "):
        key = get_representation_from_word(word,
                                           pronouns_dict,
                                           verbs_dict,
                                           keywords_dict)
        scores += get_word_score(key, weights_df)
    return scores
    

def get_representation_from_word(word,
                                 pronouns_dict,
                                 verbs_dict,
                                 keywords_dict):
    for key in pronouns_dict.keys():
        if word in pronouns_dict[key]:
            return key
    
    for key in verbs_dict.keys():
        if word in verbs_dict[key]:
            return key
        
    for key in keywords_dict.keys():
        if word in keywords_dict[key]:
            return key
    
    return ""
        
def get_word_score(word, weights_df):
    if word in weights_df.index:
        return weights_df.loc[word].to_numpy()
    else:
        return np.zeros(len(weights_df.columns))
    

def show_answers(scores, dimensions):
    indexes = np.flip(np.argsort(scores))
    for i in indexes:
        print(dimensions[i])
    
    
def clear_question(question):
    question_processed = question.lower()
    question_processed = question_processed.replace("?","")
    question_processed = question_processed.replace("¿","")
    question_processed = question_processed.replace("\n","")
    return question_processed


def load_dataframe():
    weights_dataframe = pd.read_csv(WEIGHTS_RESULTS_CSV, 
                                    index_col="palabra",
                                    encoding="utf-8")
    return weights_dataframe


def load_dictionaries():
    pronouns_dict = get_dictionary(PRONOUNS_FILE)
    verbs_dict = get_dictionary(VERBS_FORMS_FILE)
    keywords_dict = get_dictionary(KEYWORDS_FORMS_FILE)
    return pronouns_dict, verbs_dict, keywords_dict
    

def get_dictionary(dictionary_file_name):
    my_dict = {}
    with open(dictionary_file_name, "r", encoding="utf-8") as pron_file:
        for pron in pron_file.readlines():
            if pron != "\n":
                pron = pron.replace("\n","")
                key, values = pron.split(":")
                my_dict[key] = values.split(",")
    return my_dict


if __name__ == "__main__":
    main()