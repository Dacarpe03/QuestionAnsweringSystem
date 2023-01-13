# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 18:28:30 2023

@author: Daniel
"""
import pandas as pd

QUESTIONS_PREFIX = "Preguntas/preguntas_"

PRONOUNS_FILE = "Pronombres/pronombres.txt"

VERBS_PREFIX = "Verbos/"
LISTA_VERBOS_PREFIX = "lista_verbos_por_dimension"
VERBS_FORMS_FILE = f"{VERBS_PREFIX}formas_verbos.txt"
VERBS_PER_DIMENSION_FILE = f"{VERBS_PREFIX}lista_verbos_por_dimension.txt"

KEYWORDS_PREFIX = "PalabrasClave/"
KEYWORDS_FORMS_FILE = f"{KEYWORDS_PREFIX}formas_palabras_clave.txt"
KEYWORDS_PER_DIMENSION_FILE = f"{KEYWORDS_PREFIX}lista_palabras_clave_por_dimension.txt"

WEIGHTS_RESULTS_CSV = "weights.csv"
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
    
    weights_dictionary = create_weights_dictionary(pronouns_dict)
    
    calculate_pronoun_weights(weights_dictionary, 
                              pronouns_dict)
    
    create_verb_files()
    calculate_verb_weights(weights_dictionary)
    
    create_keywords_files()
    
    print_weights(weights_dictionary)
    df = pd.DataFrame(weights_dictionary)
    df.to_csv(WEIGHTS_RESULTS_CSV)
    

def create_verb_files():
    verbs_dictionary = get_dictionary(VERBS_FORMS_FILE)
    fname = VERBS_PER_DIMENSION_FILE
    with open(fname, "w") as verb_file:
        for dimension_name in DIMENSIONS:
            dimension_questions = load_questions(dimension_name)
            line = dimension_name + ":"
            verbs_found = set()
            for question in dimension_questions:
                for verb in verbs_dictionary.keys():
                    if check_word_in_question(question, verb, verbs_dictionary):
                        verbs_found.add(verb)
            line += ",".join(verbs_found)
            line += "\n"
            verb_file.write(line)

def create_keywords_files():
    keywords_dictionary = get_dictionary(KEYWORDS_FORMS_FILE)
    fname = KEYWORDS_PER_DIMENSION_FILE
    with open(fname, "w") as keywords_file:
        for dimension_name in DIMENSIONS:
            dimension_questions = load_questions(dimension_name)
            line = dimension_name + ":"
            keywords_found = set()
            for question in dimension_questions:
                for keyword in keywords_dictionary.keys():
                    if check_word_in_question(question, keyword, keywords_dictionary):
                        keywords_found.add(keyword)
            line += ",".join(keywords_found)
            line += "\n"
            keywords_file.write(line)
    
    
def get_dictionary(dictionary_file_name):
    my_dict = {}
    with open(dictionary_file_name, "r", encoding="utf-8") as pron_file:
        for pron in pron_file.readlines():
            print(pron)
            if pron != "\n":
                pron = pron.replace("\n","")
                key, values = pron.split(":")
                my_dict[key] = values.split(",")
    return my_dict


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
                if check_word_in_question(question, pron, pronouns_dict):
                    pron_count+=1
            weight = pron_count/len(questions_list)
            weights_dictionary[dimension_name].append(weight)
            

def calculate_verb_weights(weights_dict):
    verbs_form_dict = get_dictionary(VERBS_FORMS_FILE)
    verbs_per_dimension = get_dictionary(VERBS_PER_DIMENSION_FILE)
    for verb in verbs_form_dict.keys():
        weights_dict["palabra"].append(verb)
        for dimension in DIMENSIONS:
            if verb in verbs_per_dimension[dimension]:
                weights_dict[dimension].append(2)
            else:
                weights_dict[dimension].append(0)
                
def check_word_in_question(question, word_key, word_dict):
    question_processed = clear_question(question)
    
    for word in question_processed.split(" "):
        if word in word_dict[word_key]:
            return True
    return False
    

def load_questions(dimension_name):
    question_filename = f"{QUESTIONS_PREFIX}{dimension_name}.txt"
    lines = []
    with open(question_filename, "r", encoding='utf-8') as questions:
        lines = questions.readlines()
    return lines


def clear_question(question):
    question_processed = question.lower()
    question_processed = question_processed.replace("?","")
    question_processed = question_processed.replace("¿","")
    question_processed = question_processed.replace("\n","")
    return question_processed


def print_weights(weights_dict):
    my_keys = weights_dict.keys()
    n = len(weights_dict["palabra"])
    for k in my_keys:
        row = f"{k}"
        for i in range(0,n):
            if k != "palabra":
                row += " & " + "{:.3f}".format(weights_dict[k][i])
            else:
                row += " & " + weights_dict[k][i]
        row += "\\\\ \\hline"
        print(row.replace("_", "\\_"))


def print_verbs(verbs_forms_dict):
    fname = VERBS_PER_DIMENSION_FILE
    with open(fname, "r") as verb_file:
        for line in verb_file.readlines():
            dimension, verbs = line.split(":")
            dimension = dimension.replace("_", "\\_")
            print(f"Los verbos para la dimensión \\textbf{{{dimension}}} son:")
            print("\\begin{itemize}")
            for v in verbs.replace("\n","").split(","):
                lista = "``" + "'',``".join(verbs_forms_dict[v]) + "''"
                print(f"    \\item \\textbf{{{v}}}, comprobando {lista}")
            print("\\end{itemize}")
            
if __name__ == "__main__":
    main()
    print_verbs(get_dictionary(VERBS_FORMS_FILE))