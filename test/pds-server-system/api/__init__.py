config = [{
    "piid": "pdspi-guidance-example"
}]

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


def get_config():
    return config

def post_profile(ptid, piid, timestamp, body):
    return profile
    
def post_guidance(body):
    return guidance

clinical_feature_variables = [
    {
        "clinicalFeatureVariable": "v0",
        "description": "f0",
        "title": "t0",
        "why": "w0"
    }, {
        "clinicalFeatureVariable": "v1",
        "description": "f1",
        "title": "t1",
        "why": "w1"
    }, {
        "clinicalFeatureVariable": "v2",
        "description": "f2",
        "title": "t2",
        "why": "w2"
    }
]

phenotypes = {
    "1000": [{
        "value": "a0",
        "units": "u0",
        "certitude": 0,
        "how": "c0",
    }, {
        "value": "a1",
        "units": "u1",
        "certitude": 1,
        "how": "c1",
    }, {
        "value": "a2",
        "units": "u2",
        "certitude": 2,
        "how": "c2",
    }]
}

def get_clinical_feature_variables():
    return clinical_feature_variables

def get_phenotype(ptid, fhir_plugin_id, timestamp, body):
    ps = phenotypes.get(ptid)
    if ps is None:
        return ("Not Found", 404)
    else:
        for p, cfv in zip(ps, clinical_feature_variables):
            cus = [a for a in body if a["clinicalFeatureVariable"] == cfv["clinicalFeatureVariable"]]
            if len(cus) > 0:
                q = cus[0]
                unit = q.get("units")
                if unit is not None:
                    p["units"] = unit
        return ps





