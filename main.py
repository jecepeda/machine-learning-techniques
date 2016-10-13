from os import path, remove
from datetime import datetime
from models import Incidencia, get_db_session, create_db

def clean_incidence(raw_incidence):
    result = {}
    raw_attributes = [item for item in raw_incidence.split("\n") if item != '']

    for attribute in raw_attributes:
        if ">" in attribute:
            key = extract_key(attribute)
            result[key.replace("/","")] = get_value(key, attribute)

    return result

def extract_key(attribute):
    return attribute[1:attribute.index(">")]

def get_value(key, attribute):
    words_to_remove = ["<{}>".format(key),"</{}>".format(key)]
    return replace_and_clean_data(words_to_remove, attribute)

def replace_and_clean_data(words, data):
    for item in words:
        data = data.replace(item, "")
    return data

def load_and_clean_data(path):
    data = open(path, encoding="ISO-8859-1")

    words_to_remove = ["<raiz>", "</raiz>", "</incidenciaGeolocalizada>", "\t"]
    data_cleaned = replace_and_clean_data(words_to_remove, data.read())
    data_cleaned = [line for line in data_cleaned.split("<incidenciaGeolocalizada>")][1:]

    return data_cleaned

def extract_data(data):
    result = []

    for raw_incidence in data:
        incidence_dict = clean_incidence(raw_incidence)
        result.append(incidence_dict)

    return result

def insert_incidences_into_db(incidences, db):
    for incidence in incidences:
        incidence_object = Incidencia()
        set_incidence_attributes(incidence_object, incidence, db)
    db.commit()

def set_incidence_attributes(incidence_object, incidence, db):
    if incidence['provincia'] == 'BIZKAIA':
        for key in incidence.keys():
            if incidence[key] is not '':
                incidence_object.__setattr__(key, turn_to_datatype(key, incidence[key]))
                db.add(incidence_object)
    
def turn_to_datatype(attrib, value):
    float_attrib = ["longitud", "latitud", "pk_inicial", "pk_final"]

    if attrib in float_attrib:
        return float(value)
    elif attrib == "fechahora_ini":
        return convert_to_date_time(value)
    else:
        return value

#Convierte una string a formato DateTime
#return el valor convertido
def convert_to_date_time(value):
    ret =  datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return ret


if __name__ == "__main__":
    file_data = load_and_clean_data("resources/inc2006.xml")
    incidences = extract_data(file_data)
    path_to_db = "sqlalchemy_example.db"
    
    if path.exists(path_to_db):
        remove(path_to_db)
    create_db("sqlite:///{}".format(path_to_db))
    db = get_db_session("sqlite:///{}".format(path_to_db))

    insert_incidences_into_db(incidences, db)

