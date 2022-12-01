from heapq import merge
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pickle

cred = credentials.Certificate("Data/api-redes-366215-firebase-adminsdk-2fnxp-1c0fb5faf6.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def agregar_registros(Lista_registros):
    for diccionario in Lista_registros:
        doc_ref = db.collection(u'registros_2022').document().set(diccionario)

def agregar_registros_unique(Lista_registros):
    data = {u'registros':Lista_registros}
    db.collection(u'registros_2022_unique').document().set(data)

def obtener_registros():
    with open('Data/registros_2022.json', "rb") as df:
        Lista_diccionarios = pickle.load(df)
    return Lista_diccionarios

if __name__ == "__main__":
    lista = obtener_registros()
    agregar_registros_unique(lista)