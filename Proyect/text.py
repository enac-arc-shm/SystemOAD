from heapq import merge
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pickle

cred = credentials.Certificate("Data/api-redes-366215-firebase-adminsdk-2fnxp-1c0fb5faf6.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

