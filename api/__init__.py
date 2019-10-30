import os
import requests
import sys

pds_host = os.environ["PDS_HOST"]
pds_port = os.environ["PDS_PORT"]
pds_config = os.environ["PDS_CONFIG"]
pds_url_base = f"http://{pds_host}:{pds_port}/v1/plugin"

def getAggregator(patient_id, model, model_plugin_id, timestamp):
    resp0 = requests.get(f"{pds_url_base}/{pds_config}/config")
    config = resp0.json()
    profile_plugin_id = config["profile_plugin_id"]
    data_provider_plugin_id = config["data_provider_plugin_id"]
    phenotype_mapping_plugin_id = config["phenotype_mapping_plugin_id"]
    url = f"{pds_url_base}/{profile_plugin_id}/profile?patient_id={patient_id}&model={model}&phenotype_mapping_plugin_id={phenotype_mapping_plugin_id}&data_provider_plugin_id={data_provider_plugin_id}&model_plugin_id={model_plugin_id}&timestamp={timestamp}"
    resp1 = requests.get(url)
    status_code = resp1.status_code
    if status_code != 200:
        try:
            resp = resp1.json()
        except:
            resp = resp1.text
        return {
            "url": url,
            "status_code": status_code,
            "response": resp
        }, 500
    features = resp1.json()
    url = f"{pds_url_base}/{model_plugin_id}/guidance/{model}"
    resp2 = requests.post(url, json=features)
    
    guidance = resp2.json()
    return {
        "features": features,
        "guidance": guidance
    }
            
        
