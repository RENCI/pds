clinical_feature_variables = {
    "m": [{
        "clinical_feature_variable": "v0",
        "description": "f0"
    }, {
        "clinical_feature_variable": "v1",
        "description": "f1"
    }, {
        "clinical_feature_variable": "v2",
        "description": "f2"
    }]
}

phenotypes = {
    "1000": {
        "v0": {
            "value": "a0",
            "certitude": 0,
            "calculation": "c0"
        }, "v1": {
            "value": "a1",
            "certitude": 1,
            "calculation": "c1"
        }, "v2": {
            "value": "a2",
            "certitude": 2,
            "calculation": "c2"
        }
    }
}

def get_clinical_feature_variables(model):
    return clinical_feature_variables.get(model, (404, "Not Found"))

def get_phenotype(patient_id, clinical_feature_variable, data_provider_plugin_interface, timestamp):
    phenotype = phenotypes.get(patient_id)
    if phenotype is None:
        return 404, "Not Found"
    else:
        return phenotype.get(clinical_feature_variable, (404, "Not Found"))





