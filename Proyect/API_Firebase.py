from heapq import merge
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

cred = credentials.Certificate("Proyect/Data/api-redes-366215-firebase-adminsdk-2fnxp-1c0fb5faf6.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_date():
    now = datetime.now()
    date = str(now.day) + str(now.month) + str(now.year)
    return date
 
def agregar_registros_lista(collection, Lista_registros):
    diccionario = {}
    contador = 1
    for registro in Lista_registros:
        diccionario[f"Registro {contador}"] = registro
        contador += 1
    db.collection(collection).document(get_date()).set(diccionario)

def agregar_registros_lista_unique(title,collection, Lista_registros):
    data = {title:Lista_registros}
    db.collection(collection).document(get_date()).set(data)

def agregar_registros_diccionario(collection, data):
    db.collection(collection).document(get_date()).set(data)

def agregar_registros_diccionarios(title, collection, data):
    data_users = {title:data}
    db.collection(collection).document(get_date()).set(data_users)