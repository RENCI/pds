import requests

json_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def test_api():
    result=requests.get("http://pdsaggregator:8080/guidance?model=m&patient_id=0&model_plugin_id=mp&timestamp=2019-10-30T00:00:00Z", headers=json_headers)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == {
        "features": [{
            "value": "a0",
            "calculation": "c0",
            "certitude": 0,
            "description": "f0",
            "clinical_feature_variable": "v0"
        }, {
            "value": "a1",
            "calculation": "c1",
            "certitude": 1,
            "description": "f1",
            "clinical_feature_variable": "v1"
        }, {
            "value": "a2",
            "calculation": "c2",
            "certitude": 2,
            "description": "f2",
            "clinical_feature_variable": "v2"
        }],
        "guidance": "g1"
    }
    
