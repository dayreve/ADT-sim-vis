from pymongo import MongoClient

URI = 'mongodb://<user>:<pass>@ds115546.mlab.com:15546/fhir_db'
CLIENT = MongoClient(URI)
DB_NAME = 'fhir_db'
DB = CLIENT.fhir_db
PATIENTS = DB.patients
WARDS = DB.wards
BEDS = DB.beds
ENCOUNTERS = DB.encounters
OBS = DB.observations
