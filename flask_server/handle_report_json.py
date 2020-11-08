import json, random, requests

def getRiskFactors(jsonDocument):
    risk_json = {}
    risk_json['age'] = jsonDocument['age']
    risk_json['sex'] = jsonDocument['sex']
    risk_json['hgt'] = jsonDocument['height']
    risk_json['wgt'] = jsonDocument['weight']
    risk_json['eth'] = jsonDocument['race']
    smoke = 1 if "smokinghistory" in jsonDocument['respiratory'] else 0
    return risk_json, smoke

def calcRiskVector(jsonDoc, rand=True):
    if rand:
        ret_json = {
            "clip": False,
            "risks": [
                {
                    "condition": "all-cause",
                    "type": "mortality",
                    "index": random.uniform(0, 100),
                    "ratio": random.random() * random.uniform(0, 100),
                    "zscore": random.uniform(-1000, 1000),
                    "percentile": random.uniform(0, 10000) / 100
                }
            ]
        }
        return json.dumps(ret_json)
    riskFactors = getRiskFactors(jsonDoc)
    request_body = {
        "mhm": riskFactors[0],
        "smk": {"evr": riskFactors[1]},
        "clip": False
    }
    headers = {'X-dacadoo-Key': 'IZvxEg5Dc78yT5qJZLDaBfYSmknOPisS8HTNGBQh'}

    r = request.post("https://models.dacadoo.com/risk/3", data=request_body, headers=headers)
    return r.json()
