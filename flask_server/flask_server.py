import flask, json, sys
import cloudant_db, handle_report_json

app = flask.Flask(__name__)

# Patients databases interactions 
@app.route("/api/database_interaction/patient", methods=['GET'])
def getPatient():
    if 'patient_id' in flask.request.args:
        if flask.request.args['patient_id'] == "all":
            return cloudant_db.getAllPatientIDs()
        else:
            requestDoc = {'patient_id': str(flask.request.args['patient_id'])}
            return flask.jsonify(cloudant_db.query_patient(requestDoc, 'patient_information'))
    return flask.jsonify({"Error": "No patient ID. Please specify"}), 400
    


@app.route("/api/database_interaction/patient/new", methods=['POST'])
def newPatient():
    if not flask.request.json or 'patient_id' not in flask.request.json or 'patient_risk_level' not in flask.request.json or 'patient_at_risk_of' not in flask.request.json:
        return flask.jsonify({"Error": "Missing information. Please ensure complete patient information"}), 400
    
    try:
        cloudant_db.create_patientdoc(flask.request.json, "patient_information")
    except KeyError:
        return flask.jsonify({"Error": "Missing information. Please ensure complete patient information"}), 400
    finally:
        return flask.jsonify({"Status": "success"})

@app.route("/api/database_interaction/patient", methods=['POST'])
def updatePatient():
    if not flask.request.json or 'patient_id' not in flask.request.json or 'db_name' not in flask.request.args:
        return flask.jsonify({"Error": "Missing information. Please ensure complete patient information"}), 400

    db_name = str(flask.request.args['db_name'])
    cloudant_db.update_doc(flask.request.json,db_name)

    return flask.jsonify({"Status": "success"})

@app.route("/api/database_interaction/patient/delete", methods=['POST'])
def removePatient():
    if 'patient_id' in flask.request.args and 'delete' in flask.request.args and 'db_name' in flask.request.args:
        requestDoc = {'patient_id': str(flask.request.args['patient_id'])}
        db_name = str(flask.request.args['db_name'])
        cloudant_db.delete_doc(requestDoc,db_name)
        return flask.jsonify({"Status": "success"})
    else:
        return flask.jsonify({"Error": "Missing information. Please ensure complete patient information"}), 400


@app.route("/api/database_interaction/report", methods=['POST'])
def reportSympts():
    if 'patient_id' not in flask.request.json:
        return flask.jsonify({"Error": "Missing information. Please ensure complete patient information"}), 400
    
    risk_json = handle_report_json.calcRiskVector(flask.request.json, True)
    risk_json = json.loads(risk_json)
    risk_json = {"patient_id": flask.request.json['patient_id'], "doctor_id": flask.request.json['doctor_id'], "risk_evaluations": [risk_json]}
    cloudant_db.saveRiskProfile(json.dumps(risk_json), 'risk_information')
    return flask.jsonify(risk_json)
    
# Doctor appointment database interactions
@app.route("/api/database_interaction/doctor", methods=['GET'])
def getAppts():
    if 'doctor_id' in flask.request.args and 'db_name' in flask.request.args :
        requestDoc = {'id': str(flask.request.args['id'])}
        db_name    = str(flask.request.args['db_name'])
        return flask.jsonify(cloudant_db.getAppointments(requestDoc,db_name))
    else:
        return flask.jsonify({"Error": "Missing information. Please ensure complete patient information"}), 400

@app.route("/api/database_interaction/doctor", methods=['POST'])
def setApps():
    if 'risk_score' not in flask.request.json or 'date' not in flask.request.json or 'db_name' not in flask.request.json:
         return flask.jsonify({"Error": "Missing information. Please ensure complete patient information"}), 400

    db_name = str(flask.request.args['db_name'])
    requestDoc = {'risk_score': str(flask.request.args['risk_score']),'date': str(flask.request.args['date'])}
    cloudant_db.add_appointments(requestDoc,db_name) 

    return flask.jsonify({"Status": "success"})

@app.route("/api/database_interaction/internal", methods=['GET'])
def getRiskProfile():
    if 'patient_id' not in flask.request.args:
        return flask.jsonify({"Error": "Missing information. Please ensure complete patient information"}), 400
    
    functionJSON = {'patient_id': str(flask.request.args['patient_id'])}
    ret_doc = cloudant_db.getRiskProfile(json.dumps(functionJSON), 'risk_information')
    return flask.jsonify(ret_doc)

