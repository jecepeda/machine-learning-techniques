
# coding: utf-8

# In[1]:

# basic packages
from os import path, remove
from datetime import datetime

# load models
import sys
sys.path.append('../')
from database.models import Incidencia, get_db_session, create_db


# In[2]:

def clean_data(words, data):
    '''
    Get an string and return a
    string without the words passed by arguments
    '''
    for item in words:
        data = data.replace(item, "")
    return data


# In[3]:

def load_file(file_path, coding="UTF-8"):
    '''
    load the file given an encoding
    '''
    return open(file_path, encoding=coding).read()


# In[4]:

def split_file(data_file, token="<incidenciaGeolocalizada>", start_index=1):
    '''
    Split the file into tokens and returns the list starting at a given index
    '''
    return [line for line in data_file.split(token)][start_index:]


# In[5]:

def insert_incidences_into_db(incidences, session):
    '''
    Get the incidence objects and insert into the db
    '''
    for incidence in incidences:
        incidence_object = Incidencia()
        set_incidence_attributes(incidence_object, incidence, session)

    session.commit()


# In[6]:

def set_incidence_attributes(incidence_object, incidence, session, province='BIZKAIA'):
    '''
    Get the incidence dict, creates the Incidence object,
    set the Incidence attributes and add to the db
    '''
    if incidence['provincia'] == province:
        for key in incidence.keys():
            if incidence[key] is not '':
                incidence_object.__setattr__(key, turn_to_datatype(key, incidence[key]))
                session.add(incidence_object)


# In[7]:

def turn_to_datatype(attrib, value):
    '''
    get the attribute name and the value, and depending of the name,
    return the corresponding value with its corresponding type
    '''
    float_attrib = ["longitud", "latitud", "pk_inicial", "pk_final"]

    if attrib in float_attrib:
        return float(value)
    elif attrib == "fechahora_ini":
        return convert_to_date_time(value)
    else:
        return value


# In[8]:

def convert_to_date_time(value):
    '''
    You know
    '''
    ret = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return ret


# In[9]:

def clean_incidence(raw_incidence):
    '''
    Obtain the incidences in xml and return the
    same incidences in a dict format
    '''
    result = {}
    raw_attributes = [item for item in raw_incidence.split("\n") if item != '']

    for attribute in raw_attributes:
        if ">" in attribute:
            key = extract_key(attribute)
            result[key.replace("/", "")] = get_value(key, attribute)
    return result


# In[10]:

def extract_key(attribute):
    '''
    obtain the key of an xml i.e.
    <foo>Bar</foo> the key is foo
    '''
    return attribute[1:attribute.index(">")]


# In[11]:

def get_value(key, attribute):
    '''
    obtain the value of an xml i.e.
    <foo>Bar</foo> the value is Bar
    '''
    words_to_remove = ["<{}>".format(key), "</{}>".format(key)]
    return clean_data(words_to_remove, attribute)


# In[12]:

def extract_data(data):
    '''
    Obtain de data without useless words and splitted by
    a given token, and return a list of dicts representing
    the information
    '''
    result = []

    for raw_incidence in data:
        incidence_dict = clean_incidence(raw_incidence)
        result.append(incidence_dict)

    return result


# In[15]:

def get_incidences_from_xml(f_path):
    '''
    Open the file, clean the file and insert
    every item into the db
    '''
    file_r = load_file(f_path, coding="ISO-8859-1")
    words_to_remove = ["<raiz>", "</raiz>", "</incidenciaGeolocalizada>", "\t"]
    data_cleaned = clean_data(words_to_remove, file_r)
    raw_incidences = split_file(data_cleaned)

    incidences = extract_data(raw_incidences)
    path_to_db = "../incidences.db"

    if path.exists(path_to_db):
        remove(path_to_db)
    create_db("sqlite:///{}".format(path_to_db))

    session = get_db_session("sqlite:///{}".format(path_to_db))

    insert_incidences_into_db(incidences, session)


# In[16]:

get_incidences_from_xml("../data/inc2006.xml")

