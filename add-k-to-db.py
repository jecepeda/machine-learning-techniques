from models import get_db_session, Incidencia, Cluster
from sklearn.cluster import DBSCAN as dbscan
from sqlalchemy import func

def get_all_accidents(session):
    return s.query(Incidencia.longitud,
                   Incidencia.latitud,
                   Incidencia.id).filter(
                       Incidencia.tipo == 'Accidente').all()

def obtain_dbscan_labels(session, accidents, eps, minimum_points):
    dbs = dbscan(eps=eps, min_samples=minimum_points)
    return dbs.fit_predict(accidents)

def insert_values_in_incidences(session, accidents, labels):
    for idx in range(len(accidents)):
        id = accidents[idx][2]
        incidence = session.query(Incidencia).filter(Incidencia.id == id).first()
        incidence.num_cluster = labels[idx]
    session.commit()

def insert_cluster_values(session):
    clusters = session.query(Incidencia.num_cluster).distinct().all()[1:]
    print(clusters)
    for cluster in clusters:
        cl = Cluster(num_cluster=cluster[0])
        cl.accidents = s.query(func.count(Incidencia.id)).filter(
            Incidencia.num_cluster == cluster[0]).first()[0]
        cl.nivel_medio = s.query(func.max(Incidencia.nivel)).filter(
            Incidencia.num_cluster == cluster[0],
            Incidencia.nivel != 'unknown').first()[0]
        cl.causa_ppal = s.query(func.max(Incidencia.causa)).filter(
            Incidencia.num_cluster == cluster[0],
            Incidencia.causa != 'unknown').first()[0]
        cl.carretera = s.query(func.max(Incidencia.carretera)).filter(
            Incidencia.num_cluster == cluster[0],
            Incidencia.carretera != 'unknown').first()[0]
        session.add(cl)
    session.commit()

s = get_db_session('sqlite:///incidences.db')
accidents = get_all_accidents(s)
print(len(accidents))
lat_and_lon = [accident[0:2] for accident in accidents]
labels = obtain_dbscan_labels(s, lat_and_lon, eps=0.01, minimum_points=10)
insert_values_in_incidences(s, accidents, labels)
insert_cluster_values(s)
print(labels)
