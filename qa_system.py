# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 18:28:30 2023

@author: Daniel
"""
import pandas as pd

QUESTIONS_PREFIX = "Preguntas/preguntas_"
PRONOUNS_FILE = "Pronombres/pronombres.txt"
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


def main():
    pronouns_dict = get_dictionary(PRONOUNS_FILE)
    print(pronouns_dict)
    weights_dictionary = create_weights_dictionary(pronouns_dict)
    
    calculate_pronoun_weights(weights_dictionary, 
                              pronouns_dict)
    
    print(weights_dictionary)
    df = pd.DataFrame(weights_dictionary)
    df.to_csv('prueba.csv')
    

def get_dictionary(dictionary_file_name):
    pronouns_dict = {}
    with open(dictionary_file_name, "r", encoding="utf-8") as pron_file:
        for pron in pron_file.readlines():
            pron = pron.replace("\n","")
            key, values = pron.split(":")
            pronouns_dict[key] = values.split(",")
    return pronouns_dict


def create_weights_dictionary(pronouns_dict):
    weights_dictionary = {"palabra": []}
    for pron in pronouns_dict.keys():
        weights_dictionary["palabra"].append(pron)
        
    for dimension in DIMENSIONS:
        weights_dictionary[dimension] = []
    return weights_dictionary


def calculate_pronoun_weights(weights_dictionary, pronouns_dict):
    for pron in pronouns_dict.keys():
        for dimension_name in DIMENSIONS:
            pron_count = 0
            questions_list = load_questions(dimension_name)
            for question in questions_list:
                if check_question_pronoun(question, pron, pronouns_dict):
                    pron_count+=1
            weight = pron_count/len(questions_list)
            weights_dictionary[dimension_name].append(weight)
            

def check_question_pronoun(question, pronoun_key, pronouns_dict):
    question_processed = question.lower()
    question_processed = question_processed.replace("?","")
    question_processed = question_processed.replace("¿","")
    
    for word in question_processed.split(" "):
        print(word)
        if word in pronouns_dict[pronoun_key]:
            return True
    return False
    
def load_questions(dimension_name):
    question_filename = f"{QUESTIONS_PREFIX}{dimension_name}.txt"
    lines = []
    with open(question_filename, "r", encoding='utf-8') as questions:
        lines = questions.readlines()
    return lines


if __name__ == "__main__":
    main()