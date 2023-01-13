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

ELON_ANSWERS = "Respuestas/respuestas_elon.txt"
STEVE_ANSWERS = "Respuestas/respuestas_steve.txt"


def main():
    weights_df = load_dataframe()
    pronouns_dict, verbs_dict, keywords_dict = load_words_dictionaries()
    elon_dict = get_dictionary(ELON_ANSWERS)
    steve_dict = get_dictionary(STEVE_ANSWERS)
    personalities_dict = {"elon":elon_dict, "steve":steve_dict}
    dimensions = weights_df.columns
    n_dimensions = len(dimensions)
    while True:
        question = get_question()
        personality = detect_personality(question)
        if personality in personalities_dict.keys():
            scores_array = get_question_scores(question, 
                                           weights_df, 
                                           n_dimensions,
                                           pronouns_dict,
                                           verbs_dict,
                                           keywords_dict)
            show_answers(scores_array,
                         dimensions, 
                         personalities_dict[personality])
        
        
def get_question():
    question = input("Por favor, introduce una pregunta acerca de Elon Musk o Steve Jobs:\n")
    question = clear_question(question)
    return question


def detect_personality(question):
    has_elon = False
    has_steve = False
    for word in question.split(" "):
        if word in ["elon", "musk"]:
            has_elon = True
        if word in ["steve", "jobs"]:
            has_steve = True
    
    if has_elon and has_steve:
        print("No reconocemos a la personalidad por la que pregunta, por favor, pregunte acerca de Elon Musk o Steve Jobs")
        return ""
    elif has_elon:
        return "elon"
    elif has_steve:
        return "steve"
    else:
        print("No reconocemos a ninguna personalidad en la pregunta, por favor pregunte acerca de Elon Musk o Steve Jobs")
        return ""

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
    

def show_answers(scores, dimensions, answers_dict):
    indexes = np.flip(np.argsort(scores))
    print("Respuestas de mayor a menor probabilidad (sólo se muestran 3):")
    for i in range(0,3):
        dim_index = indexes[i]
        dim = dimensions[dim_index]
        concat = ",".join(answers_dict[dim])
        answer = f"    Dimensión {dim}: {concat}"
        print(answer)

    
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


def load_words_dictionaries():
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