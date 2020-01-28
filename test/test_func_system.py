import requests

config = [{"piid":"pdspi-guidance-example"}]

profile = [
    {
        "value": "a0",
        "units": "u0",
        "how": "c0",
        "certitude": 0,
        "variableType": {        
            "title": "t0",
            "description": "f0",
            "clinicalFeatureVariable": "v0",
            "why": "w0"
        }
    }, {
        "value": "a1",
        "units": "u1",
        "how": "c1",
        "certitude": 1,
        "variableType": {
            "title": "t1",
            "description": "f1",
            "clinicalFeatureVariable": "v1",
            "why": "w1"
        }
    }, {
        "value": "a2",
        "units": "u2",
        "how": "c2",
        "certitude": 2,
        "variableType": {
            "title": "t2",
            "description": "f2",
            "clinicalFeatureVariable": "v2",
            "why": "w2"
        }
    }
]

guidance = {
    "title" : "guidance title",
    "id": "guidance id",
    "justification": profile,
    "cards": [
    ]
}

json_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def test_api_guidance():
    result=requests.post("http://pdsaggregator:8080/guidance", json={
        "ptid" : "0",
        "piid" : "pdspi-guidance-example",
        "timestamp": "2019-10-30T00:00:00Z"
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
    result=requests.post("http://pdsaggregator:8080/profile", json = {
        "ptid": "1000",
        "piid": "pdspi-guidance-example",
        "timestamp": "2019-10-30T00:00:00Z",
        "mapper_plugin_id": "pdspi-mapper-example",
        "fhir_plugin_id": "pdspi-fhir-example"
    }, headers=json_headers, verify=False)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == profile


def test_api_profile_404_to_500():
    result=requests.post("http://pdsaggregator:8080/profile", json = {
        "ptid": "0",
        "piid": "pdspi-guidance-example",
        "timestamp": "2019-10-30T00:00:00Z",
        "mapper_plugin_id": "pdspi-mapper-example",
        "fhir_plugin_id": "pdspi-fhir-example"
    }, headers=json_headers, verify=False)
    print(result.content)
    assert result.status_code == 500
                
def test_ui():
    resp = requests.get("http://pdsaggregator:8080/ui")

    assert resp.status_code == 200
