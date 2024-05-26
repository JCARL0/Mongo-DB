import numpy as np
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from collections import defaultdict

def connect_database():
    client = MongoClient("mongodb+srv://JCARLO:123@contaminacionbcn.eiic72l.mongodb.net/?retryWrites=true&w=majority&appName=contaminacion", server_api=ServerApi('1'))
    return client["ContaminacionBCN"], client

def search_results(neighborhood, date):
    db, client = connect_database()
    station_id = db.Estaciones.find_one({"Nom_barri": neighborhood}).get("Estacio")
    results = []

    if station_id:
        for result in db.CalidadAire.find({"ESTACIO": station_id, "DIA": date}):
            contaminant = db.Contaminantes.find_one({"Codi_Contaminant": result["CODI_CONTAMINANT"]})
            results.append({"result": result["H12"], "desc": contaminant["Desc_Contaminant"], "unit": contaminant["Unitats"]})

    client.close()
    return results if results else None

def get_neighborhood_list():
    db, client = connect_database()
    neighborhoods = db.Estaciones.distinct("Nom_barri")
    client.close()
    return neighborhoods

def calculate_statistics(results):
    stats = defaultdict(lambda: {"values": [], "mean": 0, "max": 0, "min": 0})
    for data in results:
        if data["result"]:
            value = float(data["result"])
            stats[data["desc"]]["values"].append(value)

    for key, values in stats.items():
        if values["values"]:
            values["mean"], values["max"], values["min"] = np.mean(values["values"]), np.max(values["values"]), np.min(values["values"])
    
    return stats

def generate_chart(stats, neighborhood):
    pass
