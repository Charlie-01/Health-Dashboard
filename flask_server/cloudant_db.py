from cloudant import Cloudant

# authenticator = IAMAuthenticator(IBM_CLOUDANT_APIKEY)
# client = CloudantV1(authenticator=authenticator)
# client.set_service_url(IBM_CLOUDANT_URL)
# client = CloudantV1.new_instance(service_name="ibm-cloudant")

# database_name = "risk_information"

IBM_CLOUDANT_URL="https://348014a4-91de-4c56-8d88-eb995b41f568-bluemix.cloudantnosqldb.appdomain.cloud/"
IBM_CLOUDANT_APIKEY="aR49WSc7QKmx-wm7viiy7Tr8f2NcB-lGrdpsNJmpzfsc"
IBM_CLOUDANT_USERNAME="348014a4-91de-4c56-8d88-eb995b41f568-bluemix"


client = Cloudant.iam(IBM_CLOUDANT_USERNAME, IBM_CLOUDANT_APIKEY, connect=True)
database = client['risk_information']

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
def create_patientdoc(jsonDocument):
    patient_id = jsonDocument['patient_id']
    patient_risk_level = jsonDocument['patient_risk_level']
    patient_at_risk_of = jsonDocument['patient_at_risk_of'] 

    patient_info = {
        '_id': "{}".format(patient_id),
        'risk_level':  "{}".format(patient_risk_level),
        'at_risk_of': "{}".format(patient_at_risk_of)}
    return database.create_document(patient_info)


'''
Format for query
JSON Document={
    "patient_id" = 12878,
    "function"   = query
}
'''
def query_patient(jsonDocument):
    patient_id = jsonDocument['patient_id']
    my_document = database[patient_id]
    return my_document

'''
Format for delete
JSON Document={
    "patient_id" = 12878,
    "function"   = delete
}
'''
def delete_doc(jsonDocument):
    patient_id  = jsonDocument['patient_id']
    my_document = database[patient_id]
    my_document.delete()



testDoc = {
    'patient_id': 123,
    'patient_risk_level': 2,
    'patient_at_risk_of': 'Death'
}

print(query_patient({'patient_id': "123"}))