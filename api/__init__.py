import os
import requests
import sys
import syslog
import time
from oslash import Left, Right
from tx.requests.utils import get, post
from tx.functional.utils import monad_utils
from tx.fhir.utils import bundle, unbundle
from tx.logging.utils import tx_log

post_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


pds_host = os.environ["PDS_HOST"]
pds_port = os.environ["PDS_PORT"]
pds_config = os.environ["PDS_CONFIG"]
pds_version = os.environ["PDS_VERSION"]
pds_logging = os.environ["PDS_LOGGING"]
pds_url_base = f"http://{pds_host}:{pds_port}/{pds_version}/plugin"

def log(level, event, source, *args, **kwargs):
    tx_log(f"{pds_url_base}/{pds_logging}", level, event, source, *args, **kwargs)

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


def _get_custom_units():
    url = f"{pds_url_base}/{pds_config}/custom_units"
    return get(url)


def get_custom_units():
    return _get_custom_units().value


list_monad = monad_utils(lambda x: [x])
either_monad = monad_utils(Right)


def _get_records(ptid, fhir_plugin_id, timestamp):
    url_patient = f"{pds_url_base}/{fhir_plugin_id}/Patient/{ptid}"
    url_condition = f"{pds_url_base}/{fhir_plugin_id}/Condition?patient={ptid}"
    url_observation = f"{pds_url_base}/{fhir_plugin_id}/Observation?patient={ptid}"

    return get(url_patient).bind(lambda patient: get(url_condition).bind(lambda condition: get(url_observation).bind(lambda observation: unbundle(condition).bind(lambda condition_unbundled: unbundle(observation).map(lambda observation_unbundled: bundle([
        patient,
        *condition_unbundled,
        *observation_unbundled
    ]))))))
                          

    
def get_patient_variables(body):
    ptid = body["ptid"]
    piid = body["guidance_piid"]
    mapper_plugin_id = body["mapper_piid"]
    fhir_plugin_id = body["fhir_piid"]
    timestamp = body["timestamp"]
    
    def handle_clinical_feature_variables(custom_units, config):
        if len(config) > 0:
            if len(config) > 1:
                log (syslog.LOG_ERR, f"more than one configs for plugin {piid}")
            clinical_feature_variable_objects = config[0]["requiredPatientVariables"]
            def cfvo_to_cfvo2(cfvo):
                cfv = cfvo["id"]
                cfvo2 = {
                    "id": cfv
                }
                unit = cfvo.get("units")
                if unit is not None:
                    cfvo2["units"] = unit
                elif custom_units is not None:
                    cus = [a for a in custom_units if a["id"] == cfv]
                    if len(cus) != 1:
                        log(syslog.LOG_ERR, f"zeor or more than one default_units for patient variable {cfv}", "pds")
                    if len(cus) > 0:
                        cfvo2["units"] = cus[0]["units"]
                return Right(cfvo2)
            return either_monad.sequence(list(map(cfvo_to_cfvo2, clinical_feature_variable_objects)))
        else:
            return Left(f"no configs for plugin {piid}")

    def handle_mapper(cfvos2, data):
        url = f"{pds_url_base}/{mapper_plugin_id}/mapping?ptid={ptid}&fhir_plugin_id={fhir_plugin_id}&timestamp={timestamp}"
        return post(url, json={
            "patientVariables": cfvos2,
            "data": data
        })

    return _get_custom_units() \
        .bind(lambda custom_units: _get_config(piid) \
              .bind(lambda config: handle_clinical_feature_variables(custom_units, config))) \
        .bind(lambda cfvo2: _get_records(ptid, fhir_plugin_id, timestamp) \
              .bind(lambda data: handle_mapper(cfvo2, data))) \
        .value


def get_guidance(body):
    # features = get_profile(body["ptid"], body["piid"], body["timestamp"])
    piid = body["piid"]
    url = f"{pds_url_base}/{piid}/guidance"
    resp2 = post(url, json=body)
    return resp2.value
            

def get_config(piid=None):
    return _get_config(piid).value


def _get_config(piid=None):
    url = f"{pds_url_base}/{pds_config}/config"
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


def get_selectors(piid=None):
    url = f"{pds_url_base}/{pds_config}/selectors"
    resp = get(url)
    return resp.value

    
