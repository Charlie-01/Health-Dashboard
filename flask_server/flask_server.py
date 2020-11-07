import flask
import cloudant_db,json,sys

app = flask.Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello world"

@app.route("/api/database_interaction/patient", methods=['GET'])
def getPatient():
    if 'patient_id' in flask.request.args:
        requestDoc = {'patient_id': str(flask.request.args['patient_id'])}
        return flask.jsonify(cloudant_db.query_patient(requestDoc))
    else:
        return "Error: No patient ID. Please specify patient"

@app.route("/api/database_interaction/patient", methods=['POST'])
def updatePatient():
    pass

def response_to_flask(body):
    req = json.loads(body.decode('utf-8'))
    try:
        if 'function' in req:
            if req['function'] == 'create':
                cloudant_db.create_patientdoc(req)
            elif req['function'] == 'query':
                response = cloudant_db.query_patient(req)
            elif req['function'] == 'delete':
                cloudant_db.delete_doc(req)
    except Exception as e:
        print('\n---------- error -----------')
        traceback.print_exc()
        print('\n')
