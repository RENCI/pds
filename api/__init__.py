import os
import requests
import sys
from oslash import Left, Right
from tx.requests.utils import get, post
from tx.functional.utils import monad_utils


pds_host = os.environ["PDS_HOST"]
pds_port = os.environ["PDS_PORT"]
pds_config = os.environ["PDS_CONFIG"]
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
            "why": {
                "type": "string"
            },
            "units": {
                "type": "string"
            }
        },
        "required": [
            "clinicalFeatureVariable",
            "description",
            "title",
            "why"
        ]
    }
}

def get_profile(body):
    ptid = body["ptid"]
    piid = body["piid"]
    mapper_plugin_id = body["mapper_plugin_id"]
    fhir_plugin_id = body["fhir_plugin_id"]
    timestamp = body["timestamp"] 
    custom_units = body.get("default_units")
    url = f"{pds_url_base}/{piid}/clinical_feature_variables"
    resp1 = get(url, schema=cfv_schema)
    if isinstance(resp1, Left):
        return resp1.value
    clinical_feature_variable_objects = resp1.value

    def cfvo_to_cfvo2(cfvo):
        cfv = cfvo["clinicalFeatureVariable"]
        cfvo2 = {
            "clinicalFeatureVariable": cfv
        }
        unit = cfvo.get("units")
        if unit is not None:
            cfvo2["units"] = unit
        elif custom_units is not None:
            cus = [a for a in custom_units if a["clinicalFeatureVariable"] == cfv]
            if len(cus) > 0:
                cfvo2["units"] = cus[0]["units"]
        return cfvo2
    
    cfvos2 = list(map(cfvo_to_cfvo2, clinical_feature_variable_objects))

    url = f"{pds_url_base}/{mapper_plugin_id}/mapping?ptid={ptid}&fhir_plugin_id={fhir_plugin_id}&timestamp={timestamp}"
    resp2 = post(url, json=cfvos2)
    if isinstance(resp2, Left):
        return resp2.value
    value_objects = resp2.value

    profile = [{
        "variableType": clinical_feature_variable_object, **value_object
    } for value_object, clinical_feature_variable_object in zip(value_objects, clinical_feature_variable_objects)]

    return profile
            
        
def get_guidance(body):
    # features = get_profile(body["ptid"], body["piid"], body["timestamp"])
    piid = body["piid"]
    url = f"{pds_url_base}/{piid}/guidance"
    resp2 = post(url, json=body)
    return resp2.value
            
def get_config(piid=None):
    return _get_config(piid).value

list_monad = monad_utils(lambda x: [x])
either_monad = monad_utils(Right)

def _get_config(piid=None):
    url = f"http://{pds_host}:{pds_port}/v1/plugin/{pds_config}/config"
    resp = get(url)
    if isinstance(resp, Left):
        return resp
    else:
        if piid is not None:
            l = list(filter(lambda x : x["piid"] == piid, resp.value))
            if len(l) == 0:
                return Left(("not found", 404))
            else:
                return Right(l)
        else:
            return resp
        
    
