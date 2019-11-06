config = {
    "aggregator_plugin_id": "pds-aggregator",
    "phenotype_mapping_plugin_id": "pds-phenotype-mapping",
    "data_provider_plugin_id": "pds-mock-fhir",
    "profile_plugin_id": "pp",
    "model": [{
        "drug": "d1",
        "indications": [{
            "indication": "i1",
            "model_plugin_id": "pdsmpi-ref"
        }]
    }]
}

profile = [{
    "value": "a0",
    "calculation": "c0",
    "certitude": 0,
    "description": "f0",
    "clinical_feature_variable": "v0",
    "quantity": "q0",
    "timestamp": "ts0"
}, {
    "value": "a1",
    "calculation": "c1",
    "certitude": 1,
    "description": "f1",
    "clinical_feature_variable": "v1",
    "quantity": "q1",
    "timestamp": "ts1"
}, {
    "value": "a2",
    "calculation": "c2",
    "certitude": 2,
    "description": "f2",
    "clinical_feature_variable": "v2",
    "quantity": "q2",
    "timestamp": "ts2"
}]

def get_config():
    return config

def get_profile(patient_id, model, data_provider_plugin_id, phenotype_mapping_plugin_id, model_plugin_id, timestamp):
    return profile
    
def post_guidance(model, body):
    return "g1"






