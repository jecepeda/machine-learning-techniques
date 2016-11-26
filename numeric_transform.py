from models import get_db_session, Cluster, ClusterN
from sqlalchemy import func

def tf_nivel_medio(a):
    n = 0

    if a == "Rojo":
        n = 5
    elif a == "Blanco":
        n = 1
    else:
        n = 10

    return n

def tf_causa_ppal(a):
    n = 0

    if a == "Alcance":
        n = 1
    elif a == "Salida":
        n = 3
    else :
        n = 4

    return n

def tf_carretera(a):
    n = 0

    if "BI-" in a:
        n = 1
    elif "N-" in a:
        n = 2
    else:
        n = 3

    return n

def transform_db(session):
    clusters = session.query(Cluster.id).all()[:]
    for cluster in clusters:
        cln = ClusterN(num_cluster = cluster[0])
        cln.accidents = s.query(Cluster.accidents).filter(
                Cluster.id == cluster[0]).first()[0]
        cln.nivel_medio = tf_nivel_medio(s.query(Cluster.nivel_medio).filter(
                Cluster.id == cluster[0]).first()[0])
        cln.causa_ppal = tf_causa_ppal(s.query(Cluster.causa_ppal).filter(
                Cluster.id == cluster[0]).first()[0])
        cln.carretera = tf_carretera(s.query(Cluster.carretera).filter(
                Cluster.id == cluster[0]).first()[0])
        cln.na_causa = s.query(Cluster.na_causa).filter(
                Cluster.id == cluster[0]).first()[0]

        session.add(cln)
    session.commit()

s = get_db_session('sqlite:///incidences.db')
transform_db(s)



