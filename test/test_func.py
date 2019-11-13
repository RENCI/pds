import requests

json_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def test_api():
    result=requests.get("http://pdsaggregator:8080/guidance?model=m&patient_id=0&model_plugin_id=mp&timestamp=2019-10-30T00:00:00Z", headers=json_headers, verify=False)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == {
        "features": [{
            "value": "a0",
            "title": "t0",
            "unit": None,
            "calculation": "c0",
            "certitude": 0,
            "description": "f0",
            "clinical_feature_variable": "v0",
            "quantity": None,
            "timestamp": None
        }, {
            "value": "a1",
            "title": "t1",
            "unit": None,
            "calculation": "c1",
            "certitude": 1,
            "description": "f1",
            "clinical_feature_variable": "v1",
            "quantity": None,
            "timestamp": None
        }, {
            "value": "a2",
            "title": "t2",
            "unit": None,
            "calculation": "c2",
            "certitude": 2,
            "description": "f2",
            "clinical_feature_variable": "v2",
            "quantity": None,
            "timestamp": None
        }],
        "guidance": "g1"
    }
    
