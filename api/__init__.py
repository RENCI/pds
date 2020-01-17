import os
import requests
import sys
from tx.requests.utils import get, post
from tx.oslash.utils import monad_utils
from oslash import Left, Right

pds_host = os.environ["PDS_HOST"]
pds_port = os.environ["PDS_PORT"]
pds_config = os.environ["PDS_CONFIG"]
pds_url_base = f"http://{pds_host}:{pds_port}/v1/plugin"

def get_guidance(body):
    # features = get_profile(body["ptid"], body["piid"], body["timestamp"])
    
    url = f"{pds_url_base}/{piid}/guidance"
    resp2 = post(url, json=body)
    return resp2.value
            
def get_profile(ptid, piid, timestamp):
pds_host = os.environ["PDS_HOST"]
pds_port = os.environ["PDS_PORT"]
pds_url_base = f"http://{pds_host}:{pds_port}/v1/plugin"
cfv_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "clinical_feature_variable": {
                "type": "string"
            },
            "description": {
                "type": "string"
            },
            "title": {
                "type": "string"
            },
            "unit": {
                "type": "string"
            }
        },
        "required": [
            "clinical_feature_variable",
            "description",
            "title"
        ]
    }
}

def get_profile(ptid, piid, timestamp):
    resp0 = get(f"{pds_url_base}/{pds_config}/config")
    if isinstance(resp0, Left):
        return resp0.value
    config = resp0.value
    phenotype_mapping_plugin_id = config["phenotype_mapping_plugin_id"]
    data_provider_plugin_id = config["data_provider_plugin_id"]
    custom_units = config.get("default_units")
    url = f"{pds_url_base}/{piid}/clinical_feature_variables"
    resp1 = get(url, schema=cfv_schema)
    if isinstance(resp1, Left):
        return resp1.value
    clinical_feature_variable_objects = resp1.value

    def cfvo_to_cfvo2(cfvo):
        cfv = cfvo["clinical_feature_variable"]
        cfvo2 = {
            "clinical_feature_variable": cfv
        }
        unit = cfvo.get("unit")
        if unit is not None:
            cfvo2["unit"] = unit
        elif custom_units is not None:
            cus = [a for a in custom_units if a["clinical_feature_variable"] == cfv]
            if len(cus) > 0:
                cfvo2["unit"] = cus[0]["unit"]
        return cfvo2
    
    cfvos2 = list(map(cfvo_to_cfvo2, clinical_feature_variable_objects))

    url = f"{pds_url_base}/{phenotype_mapping_plugin_id}/mapping?patient_id={ptid}&data_provider_plugin_id={data_provider_plugin_id}&timestamp={timestamp}"
    resp2 = post(url, json=cfvos2)
    if isinstance(resp2, Left):
        return resp2.value
    value_objects = resp2.value

    profile = [{
        "variableType": clinical_feature_variable_object, **value_object
    } for value_object, clinical_feature_variable_object in zip(value_objects, clinical_feature_variable_objects)]

    return profile
            
        
    resp0 = get(f"{pds_url_base}/{pds_config}/config")
    if isinstance(resp0, Left):
        return resp0.value
    config = resp0.value
    custom_units = config.get("custom_units")
    profile_plugin_id = config["profile_plugin_id"]
    data_provider_plugin_id = config["data_provider_plugin_id"]
    phenotype_mapping_plugin_id = config["phenotype_mapping_plugin_id"]
    url = f"{pds_url_base}/{profile_plugin_id}/profile?patient_id={ptid}&model_plugin_id={piid}&timestamp={timestamp}"
    resp1 = post(url, json=config)
    return resp1.value
            
def get_config(piid=None):
    return _get_config(piid).value

list_monad = monad_utils(lambda x: [x])
either_monad = monad_utils(Right)

def _get_config(piid=None):
    if piid is not None:
        return get(f"{pds_url_base}/{piid}/config").map(list_monad.pure)
    else:
        url0 = f"http://{pds_host}:{pds_port}/v1/admin/plugin"
        resp0 = get(url0)
        if isinstance(resp0, Left):
            return resp0
        else:
            plugins = resp0.value
            return either_monad.sequence(list(map(lambda plugin: get_config(plugin["name"]), plugins)))

    
