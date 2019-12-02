import requests

json_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def test_api_guidance():
    result=requests.get("http://pdsaggregator:8080/guidance?model=m&patient_id=0&model_plugin_id=mp&timestamp=2019-10-30T00:00:00Z", headers=json_headers, verify=False)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == {
        "features": [{
            "value": "a0",
            "unit": "u0",
            "title": "t0",
            "calculation": "c0",
            "certitude": 0,
            "description": "f0",
            "clinical_feature_variable": "v0",
        }, {
            "value": "a1",
            "unit": "u1",
            "title": "t1",
            "calculation": "c1",
            "certitude": 1,
            "description": "f1",
            "clinical_feature_variable": "v1",
        }, {
            "value": "a2",
            "unit": "u2",
            "title": "t2",
            "calculation": "c2",
            "certitude": 2,
            "description": "f2",
            "clinical_feature_variable": "v2",
        }],
        "guidance": "g1"
    }
    
def test_api_profile():
    result=requests.get("http://pdsaggregator:8080/profile?patient_id=0&model_plugin_id=mp&timestamp=2019-10-30T00:00:00Z", headers=json_headers, verify=False)
    print(result.content)
    assert result.status_code == 200
                
    assert result.json() == [
        {
            "value": "a0",
            "unit": "u0",
            "title": "t0",
            "calculation": "c0",
            "certitude": 0,
            "description": "f0",
            "clinical_feature_variable": "v0",
        }, {
            "value": "a1",
            "unit": "u1",
            "title": "t1",
            "calculation": "c1",
            "certitude": 1,
            "description": "f1",
            "clinical_feature_variable": "v1",
        }, {
            "value": "a2",
            "unit": "u2",
            "title": "t2",
            "calculation": "c2",
            "certitude": 2,
            "description": "f2",
            "clinical_feature_variable": "v2",
        }
    ]
    
