from cloudant import Cloudant
from cloudant.result import Result, ResultByKey
import json
from datetime import datetime
import handle_report_json

# authenticator = IAMAuthenticator(IBM_CLOUDANT_APIKEY)
# client = CloudantV1(authenticator=authenticator)
# client.set_service_url(IBM_CLOUDANT_URL)
# client = CloudantV1.new_instance(service_name="ibm-cloudant")

# database_name = "risk_information"

IBM_CLOUDANT_URL="https://348014a4-91de-4c56-8d88-eb995b41f568-bluemix.cloudantnosqldb.appdomain.cloud/"
IBM_CLOUDANT_APIKEY="aR49WSc7QKmx-wm7viiy7Tr8f2NcB-lGrdpsNJmpzfsc"
IBM_CLOUDANT_USERNAME="348014a4-91de-4c56-8d88-eb995b41f568-bluemix"


client = Cloudant.iam(IBM_CLOUDANT_USERNAME, IBM_CLOUDANT_APIKEY, connect=True)


'''
Format for create
JSON Document={
    "patient_id"         = 12878,
    "function"           = create,
    "patient_risk_level" = low/medium/high,
    "patient_at_risk_of" = DISEASE NAME
}
'''
# def create_patientdoc(patient_id,patient_risk_level,patient_at_risk_of):
def create_patientdoc(jsonDocument, database):
    database   = client[database]
    patient_id = jsonDocument['patient_id']
    patient_risk_level = jsonDocument['patient_risk_level']
    patient_at_risk_of = jsonDocument['patient_at_risk_of'] 

    patient_info = {
        '_id': "{}".format(patient_id),
        'patient_risk_level':  "{}".format(patient_risk_level),
        'patient_at_risk_of': "{}".format(patient_at_risk_of)}
    return database.create_document(patient_info)


'''
Format for query
JSON Document={
    "patient_id" = 12878,
    "function"   = query
}
'''
def query_patient(jsonDocument, database):
    database   = client[database]
    patient_id = jsonDocument['patient_id']
    if patient_id in database: return database[patient_id]
    else: return {"Error": "No patient with specified ID"}

'''
Format for delete
JSON Document={
    "patient_id" = 12878,
    "function"   = delete
}
'''
def delete_doc(jsonDocument, database):
    database    = client[database]
    patient_id  = jsonDocument['patient_id']
    my_document = database[patient_id]
    my_document.delete()

def checkPatientExists(jsonDocument, database):
    database = client[database]
    doc_key  = jsonDocument['patient_id']
    return doc_key in database

def getAllPatientIDs(database='patient_information'):
    database = client[database]
    patients = []
    for patient in Result(database.all_docs, include_docs=True):
        patients.append(patient)
    
    return json.dumps(patients)


def saveRiskProfile(jsonDocument, database):
    database = client[database]
    riskProfile = json.loads(jsonDocument)
    riskProfile['_id'] = str(riskProfile['patient_id'])

    print(riskProfile)

    time = str(datetime.utcnow())

    appt_json = {
        'risk_score': riskProfile['risk_evaluations'][0]['risks'][0]['index'],
        'date': time,
        'patient_id': riskProfile['_id']
    }

    add_appointments(json.dumps(appt_json), "doctor_appointments")

    riskProfile['risk_evaluations'][0]['report_time'] = time

    if riskProfile['_id'] in database:
        database[riskProfile['_id']]['risk_evaluations'].append(riskProfile['risk_evaluations'][0])
        database[riskProfile['_id']].save()
        client['patient_information'][riskProfile['_id']]['patient_risk_level'] = riskProfile['risk_evaluations'][0]['risks'][0]['index']
        client['patient_information'][riskProfile['_id']]['patient_at_risk_of'] = riskProfile['risk_evaluations'][0]['risks'][0]['type']

        client['patient_information'][riskProfile['_id']].save()

        print("aslkd;fjas;lkdgjakhsdgf;lkajsdg;lkjs;l")
    else:
        pat_json = {
            'patient_id': riskProfile['_id'],
            'patient_risk_level': riskProfile['risk_evaluations'][0]['risks'][0]['index'],
            'patient_at_risk_of': riskProfile['risk_evaluations'][0]['risks'][0]['type']
        }
        create_patientdoc(json.dumps(pat_json), 'patient_information')
        return database.create_document(riskProfile)

def getRiskProfile(jsonDocument, database):
    database = client[database]
    json_obg = json.loads(jsonDocument)
    return database[json_obg['patient_id']]

def update_doc(jsonDocument, database):
    database = client[database]
    patient_id  = jsonDocument['patient_id']
    my_document = database[patient_id]
    for key in jsonDocument:
        if key == "patient_id": continue
        my_document[key] = jsonDocument[key]
        
    my_document.save()

def getAppointments(jsonDocument, database):
    database = client[database]
    ret_doc  = {}
    for doc in Result(database.all_docs, include_docs=True):
        ret_doc[doc['id']] = doc
    return ret_doc
    
def add_appointments(jsonDocument,database):
    database = client[database]
    jsonDocument = json.loads(jsonDocument)
    risk_score = jsonDocument['risk_score']
    date       = jsonDocument['date']
    patient_id = jsonDocument['patient_id']
    
    if patient_id in database:
        database[patient_id]['risk_score'] = risk_score
        database[patient_id]['date'] = date
        database[patient_id].save()
        return database[patient_id]

    ret_doc = {
        'date':'{}'.format(date),
        'risk_score':'{}'.format(risk_score),
        'patient_id': f'{patient_id}'
    }
    return database.create_document(ret_doc)


'''
Database names:
doctor_appointments
doctor_information
patient_information
risk_information
'''

# testJSON = '{"patient_id":22,"doctor_id":9,"age":null,"sex":null,"weight":342,"height":124,"race":1,"general":["fever","sorethroat","cough"]}'
# testJSON = json.loads(testJSON)

# risk_json = handle_report_json.calcRiskVector(testJSON, True)
# risk_json = json.loads(risk_json)
# risk_json = {"patient_id": testJSON['patient_id'], "doctor_id": testJSON['doctor_id'], "risk_evaluations": [risk_json]}
# saveRiskProfile(json.dumps(risk_json), 'risk_information')