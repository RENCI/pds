import requests

clinical_feature_variables = [
    {
        "id": "v0",
        "title": "t0",
        "why": "w0",
        "legalValues": {
            "type": "i0"
        }
    }, {
        "id": "v1",
        "title": "t1",
        "why": "w1",
        "legalValues": {
            "type": "i1"
        }
    }, {
        "id": "v2",
        "title": "t2",
        "why": "w2",
        "legalValues": {
            "type": "i2"
        }
    }
]

config = [{
    "piid": "pdspi-guidance-example",
    "pluginType": "g",
    "setting_requests": {"patientVariables": clinical_feature_variables},
    "enabled": True
}, {
    "piid": "pdspi-mapper-example",
    "pluginType": "m",
    "enabled": True
}, {
    "piid": "pdspi-fhir-example",
    "pluginType": "f",
    "enabled": True
}]

selectors = []

guidance = {
    "title": "guidance title",
    "piid": "guidance id",
    "settings_requested": {},
    "settings_used": {},
    "advanced": {},
    "cards": []
}

phenotypes = {
    "1000": [{
        "id": "v0",
        "title": "t0",
        "variableValue": {
            "value": "a0",
            "units": "u0"
        },
        "certitude": 0,
        "how": "c0",
        "timestamp": "s0"
    }, {
        "id": "v1",
        "title": "t1",
        "variableValue": {
            "value": "a1",
            "units": "u1"
        },
        "certitude": 1,
        "how": "c1",
        "timestamp": "s1"
    }, {
        "id": "v2",
        "title": "t2",
        "variableValue": {
            "value": "a2",
            "units": "u2"
        },
        "certitude": 2,
        "how": "c2",
        "timestamp": "s2"
    }]
}

json_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def test_api_guidance():
    result=requests.post("http://pdsaggregator:8080/guidance", json={
        "ptid" : "1000",
        "piid" : "pdspi-guidance-example",
        "timestamp": "2019-10-30T00:00:00Z"
    }, headers=json_headers, verify=False)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == guidance
    
def test_api_guidance_user_supplied_patient_variables():
    result=requests.post("http://pdsaggregator:8080/guidance", json={
        "ptid" : "0",
        "piid" : "pdspi-guidance-example",
        "timestamp": "2019-10-30T00:00:00Z",
        "settings_requested": {"patientVariables": []}
    }, headers=json_headers, verify=False)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == guidance
    
def test_api_config():
    result=requests.get("http://pdsaggregator:8080/config", headers=json_headers, verify=False)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == config
    
def test_api_config_piid_200():
    result=requests.get("http://pdsaggregator:8080/config?piid=pdspi-guidance-example", headers=json_headers, verify=False)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [config[0]]
    
def test_api_config_piid_404():
    result=requests.get("http://pdsaggregator:8080/config?piid=guidance", headers=json_headers, verify=False)
    print(result.content)
    assert result.status_code == 404
                
    assert result.json() == "not found"
    
def test_api_profile():
    result=requests.post("http://pdsaggregator:8080/patientVariables", json = {
        "ptid": "1000",
        "guidance_piid": "pdspi-guidance-example",
        "timestamp": "2019-10-30T00:00:00Z",
        "mapper_piid": "pdspi-mapper-example",
        "fhir_piid": "pdspi-fhir-example"
    }, headers=json_headers, verify=False)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == phenotypes["1000"]


def test_api_profile_default():
    result=requests.post("http://pdsaggregator:8080/patientVariables", json = {
        "ptid": "1000",
        "guidance_piid": "pdspi-guidance-example",
        "timestamp": "2019-10-30T00:00:00Z"
    }, headers=json_headers, verify=False)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == phenotypes["1000"]


def test_api_profile_404_to_500():
    result=requests.post("http://pdsaggregator:8080/patientVariables", json = {
        "ptid": "0",
        "guidance_piid": "pdspi-guidance-example",
        "timestamp": "2019-10-30T00:00:00Z",
        "mapper_piid": "pdspi-mapper-example",
        "fhir_piid": "pdspi-fhir-example"
    }, headers=json_headers, verify=False)
    print(result.content)
    assert result.status_code == 500
                
def test_ui():
    resp = requests.get("http://pdsaggregator:8080/ui")

    assert resp.status_code == 200
