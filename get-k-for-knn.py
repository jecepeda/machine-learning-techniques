from models import Incidencia, get_db_session, Train, Test
import sqlalchemy
import random

def get_all_accidents(session):
    return s.query([Incidencia.longitud,
                   Incidencia.latitud,
                   Incidencia.id,
                    Incidencia.num_cluster]).filter(
                       Incidencia.tipo == 'Accidente').all()

def split_database(session):
    incidences = session.query(Incidencia.id).filter(
        Incidencia.tipo == "Accidente").all()[:]
    for incidence in incidences:
        if (random.random() < 0.6):
            cln = Train()
            cln.longitud = s.query(Incidencia.longitud).filter(
                    Incidencia.id == incidence[0]).first()[0]
            cln.latitud = s.query(Incidencia.latitud).filter(
                    Incidencia.id == incidence[0]).first()[0]
            cln.num_cluster = s.query(Incidencia.num_cluster).filter(
                    Incidencia.id == incidence[0]).first()[0]

        else:
            cln = Test()
            cln.longitud = s.query(Incidencia.longitud).filter(
                    Incidencia.id == incidence[0]).first()[0]
            cln.latitud = s.query(Incidencia.latitud).filter(
                    Incidencia.id == incidence[0]).first()[0]
            cln.num_cluster = s.query(Incidencia.num_cluster).filter(
                    Incidencia.id == incidence[0]).first()[0]

        session.add(cln)

    session.commit()



s = get_db_session('sqlite:///incidences.db')
split_database(s)
