# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 18:28:30 2023

@author: Daniel
"""
import pandas as pd

QUESTIONS_PREFIX = "Preguntas/preguntas_"
DIMENSIONS = ["nombre", 
              "primer_apellido", 
              "segundo_apellido", 
              "lugar_de_nacimiento", 
              "dia_de_nacimiento", 
              "mes_de_nacimiento", 
              "anno_de_nacimiento",
              "fecha_de_nacimiento",
              "edad",
              "dia_de_fallecimiento", 
              "mes_de_fallecimiento", 
              "anno_de_fallecimiento",
              "fecha_de_fallecimiento",
              "marido",
              "esposa",
              "pareja_actual",
              "numero_de_hijos",
              "nombre_del_padre",
              "nombre_de_la_madre",
              "universidad",
              "carrera_universitaria",
              "puestos_empresariales"
              ]

PRONOUNS_LIST = ["cómo",
                 "cuál",
                 "cuán",
                 "cuándo",
                 "cuánto",
                 "dónde",
                 "qué",
                 "quién"]



def main():
    weights_dictionary = create_weights_dictionary()
    calculate_pronoun_weights(weights_dictionary)
    df = pd.DataFrame(weights_dictionary)
    df.to_csv('prueba.csv')

def create_weights_dictionary():
    weights_dictionary = {"palabra": []}
    for pron in PRONOUNS_LIST:
        weights_dictionary["palabra"].append(pron)
        
    for dimension in DIMENSIONS:
        weights_dictionary[dimension] = []
    return weights_dictionary


def calculate_pronoun_weights(weights_dictionary):
    for pron in PRONOUNS_LIST:
        for dimension_name in DIMENSIONS:
            pron_count = 0
            questions_list = load_questions(dimension_name)
            for question in questions_list:
                pronoun_found = find_pronoun(question)
                if pronoun_found == pron:
                    pron_count+=1
            weight = pron_count/len(questions_list)
            weights_dictionary[dimension_name].append(weight)


def find_pronoun(question):
    processed_sentence = question.lower()
    processed_sentence = processed_sentence.replace("¿", "")
    processed_sentence = processed_sentence.replace("?", "")
    for word in processed_sentence.split(" "):
        if word in PRONOUNS_LIST:
            return word
    return None

    
def load_questions(dimension_name):
    question_filename = f"{QUESTIONS_PREFIX}{dimension_name}.txt"
    lines = []
    with open(question_filename, "r", encoding='utf-8') as questions:
        lines = questions.readlines()
    return lines
          

def load_dictionaries():
    return


if __name__ == "__main__":
    main()