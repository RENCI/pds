import os
import requests
import sys
import syslog
import time
from urllib.parse import quote
from oslash import Left, Right
from tx.requests.utils import get, post
from tx.functional.utils import monad_utils
from tx.fhir.utils import bundle, unbundle
from tx.logging.utils import tx_log
import tx.logging.utils

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
                          

def default_mapper_plugin_id():
    return next(filter(lambda x: x["pluginType"] == "m", get_config()))["piid"]

def default_fhir_plugin_id():
    return next(filter(lambda x: x["pluginType"] == "f", get_config()))["piid"]
    
def _get_patient_variables(body):
    ptid = body["ptid"]
    piid = body["guidance_piid"]
    mapper_plugin_id = body.get("mapper_piid")
    if mapper_plugin_id == None:
        mapper_plugin_id = default_mapper_plugin_id()
        log (syslog.LOG_ERR, f"no mapper_piid, using {mapper_plugin_id}", "pds")
    fhir_plugin_id = body.get("fhir_piid")
    if fhir_plugin_id == None:
        fhir_plugin_id = default_fhir_plugin_id()
        log (syslog.LOG_ERR, f"no fhir_piid, using {fhir_plugin_id}", "pds")
    timestamp = body.get("timestamp")
    if timestamp == None:
        timestamp = tx.logging.utils.timestamp()
        log (syslog.LOG_ERR, f"no timestamp, using {timestamp}", "pds")
    
    def handle_clinical_feature_variables(config):
        if len(config) > 0:
            if len(config) > 1:
                log (syslog.LOG_ERR, f"more than one configs for plugin {piid}", "pds")
            clinical_feature_variable_objects = config[0]["settingsDefaults"]["patientVariables"]
            def cfvo_to_cfvo2(cfvo):
                cfvo2 = {**cfvo}
                return Right(cfvo2)
            return either_monad.sequence(list(map(cfvo_to_cfvo2, clinical_feature_variable_objects)))
        else:
            return Left(f"no configs for plugin {piid}")

    def handle_mapper(cfvos2, data):
        url = f"{pds_url_base}/{mapper_plugin_id}/mapping?patient_id={ptid}&timestamp={quote(timestamp)}"
        return post(url, json={
            "variableTypes": cfvos2,
            "data": data
        })

    return _get_config(piid).bind(lambda config: handle_clinical_feature_variables(config))\
        .bind(lambda cfvo2: _get_records(ptid, fhir_plugin_id, timestamp)
              .bind(lambda data: handle_mapper(cfvo2, data)))


def get_patient_variables(body):
    return _get_patient_variables(body).value


def _get_guidance(body):
    piid = body["piid"]
    mapper_piid = body.get("mapper_piid")
    fhir_piid = body.get("fhir_piid")
    if "settings_requested" not in body or "patientVariables" not in body["settings_requested"]:
        pvs = _get_patient_variables({
            "ptid": body["ptid"],
            "guidance_piid": piid,
            **({} if mapper_piid is None else {"mapper_piid": mapper_piid}),
            **({} if fhir_piid is None else {"fhir_piid": fhir_piid})
        })
        if isinstance(pvs, Left):
            return pvs
        else:
            body["settings_requested"]["patientVariables"] = pvs.value

    url = f"{pds_url_base}/{piid}/guidance"
    resp2 = post(url, json=body)
    return resp2
            

def get_guidance(body):
    return _get_guidance(body).value
            

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

    
