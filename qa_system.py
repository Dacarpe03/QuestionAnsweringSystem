# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 18:28:30 2023

@author: Daniel
"""

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

def main():
    create_dictionaries()


def create_dictionaries():
    for dimension_name in DIMENSIONS:
        load_questions()
    
def load_questions(dimension_name):
    print("a")
    question_filename = f"{QUESTIONS_PREFIX}{dimension_name}.txt"
    with open(question_filename, "r", encoding='utf-8') as questions:
        for line in questions.readlines():
            print(line)
              
def load_dictionaries():
    return

if __name__ == "__main__":
    main()