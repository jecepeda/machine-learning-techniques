from os import path, remove
from datetime import datetime
from models import Incidencia, get_db_session, create_db

#Gets an incidence and divides it in attributes, then it stores it into it's attribute into the result array
#returns the result array
def clean_incidence(raw_incidence):
    result = {}
    raw_attributes = [item for item in raw_incidence.split("\n") if item != '']

    for attribute in raw_attributes:
        if ">" in attribute:
            key = extract_key(attribute)
            result[key.replace("/","")] = get_value(key, attribute)

    return result

#return the key from an attribute
def extract_key(attribute):
    return attribute[1:attribute.index(">")]

#Removes the key from the attribute
#returns the value from the key field given
def get_value(key, attribute):
    words_to_remove = ["<{}>".format(key),"</{}>".format(key)]
    return replace_and_clean_data(words_to_remove, attribute)

#Removes every selected word in list "words" from "data"
#return the same data without those words
def replace_and_clean_data(words, data):
    for item in words:
        data = data.replace(item, "")
    return data

#Opens the file and removes the words "<raiz>, </raiz>, </incidenciaGeolocalizada> & \t"
#return the file into a vector, separated in each incidenciaGeolocalizada
def load_and_clean_data(path):
    data = open(path, encoding="ISO-8859-1")

    words_to_remove = ["<raiz>", "</raiz>", "</incidenciaGeolocalizada>", "\t"]
    data_cleaned = replace_and_clean_data(words_to_remove, data.read())
    data_cleaned = [line for line in data_cleaned.split("<incidenciaGeolocalizada>")][1:]

    return data_cleaned

#Get the data already cleaned and sorted in an array and cleans all it's incidences
#returns the concatenation of those dictionaries
def extract_data(data):
    result = []

    for raw_incidence in data:
        incidence_dict = clean_incidence(raw_incidence)
        result.append(incidence_dict)

    return result

#Gets the incidences and turns them into db objects
#it also inputs those into the db
def insert_incidences_into_db(incidences, db):

    for incidence in incidences:
        incidence_object = Incidencia()
        for key in incidence.keys():
            if incidence[key] is not '':
                incidence_object.__setattr__(key, turn_to_datatype(key, incidence[key]))
        db.add(incidence_object)
    db.commit()

#Convierte una string a float, int, DateTime, o lo mantiene en string dependiendo del attrib
#return el valor convertido o no.
def turn_to_datatype(attrib, value):
    float_attrib = ["longitud", "latitud", "pk_inicial", "pk_final"]

    if attrib in float_attrib:
        return float(value)
    elif attrib is "DateTime":
        return convert_to_date_time(value)
    else:
        return value

#Convierte una string a formato DateTime
#return el valor convertido
def convert_to_date_time(value):
    value =  datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    return value

if __name__ == "__main__":
    file_data = load_and_clean_data("resources/inc2006.xml")
    incidences = extract_data(file_data)
    path_to_db = "sqlite:///sqlalchemy_example.db"
    if path.exists(path_to_db):
        remove(path_to_db)
    else:
        create_db(path_to_db)

    db = get_db_session(path_to_db)

    insert_incidences_into_db(incidences, db)

