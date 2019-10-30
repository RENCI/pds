import os
import requests
import sys
from tx.utils import get, post
from oslash import Left, Right

pds_host = os.environ["PDS_HOST"]
pds_port = os.environ["PDS_PORT"]
pds_config = os.environ["PDS_CONFIG"]
pds_url_base = f"http://{pds_host}:{pds_port}/v1/plugin"

def getAggregator(patient_id, model, model_plugin_id, timestamp):
    resp0 = get(f"{pds_url_base}/{pds_config}/config")
    if isinstance(resp0, Left):
        return resp0.value
    config = resp0.value
    profile_plugin_id = config["profile_plugin_id"]
    data_provider_plugin_id = config["data_provider_plugin_id"]
    phenotype_mapping_plugin_id = config["phenotype_mapping_plugin_id"]
    url = f"{pds_url_base}/{profile_plugin_id}/profile?patient_id={patient_id}&model={model}&phenotype_mapping_plugin_id={phenotype_mapping_plugin_id}&data_provider_plugin_id={data_provider_plugin_id}&model_plugin_id={model_plugin_id}&timestamp={timestamp}"
    resp1 = get(url)
    if isinstance(resp1, Left):
        return resp1.value
    features = resp1.value
    url = f"{pds_url_base}/{model_plugin_id}/guidance/{model}"
    resp2 = post(url, json=features)
    if isinstance(resp2, Left):
        return resp2.value
    guidance = resp2.value
    return {
        "features": features,
        "guidance": guidance
    }
            
        
