import requests
import time

config = {"piids":["pdspi-guidance-example","pdspi-mapper-example","pdspi-fhir-example"],"selectors":[{"title":"Drug","id":"dosing.rxCUI","legalValues":{"type":"string","enum":[{"value":"rxCUI:1596450","title":"Gentamicin"},{"value":"rxCUI:1114195"},{"value":"rxCUI:1546356"},{"value":"rxCUI:1364430"},{"value":"rxCUI:1599538"},{"value":"rxCUI:1927851"}]}}],"custom_units":[{"id": "LOINC:2160-0", "units": "mg/dL"},{"id": "LOINC:30525-0", "units": "year"},{"id": "LOINC:8302-2", "units": "m"},{"id": "LOINC:29463-7", "units": "kg"},{"id": "LOINC:39156-5", "units": "kg/m^2"}]}


time.sleep(60)

def test_get_custom_units():
    resp = requests.get("http://localhost:8080/v1/plugin/pdspi-config/customUnits")

    assert resp.status_code == 200
    assert resp.json() == config["custom_units"]


def test_get_selectors():
    resp = requests.get("http://localhost:8080/v1/plugin/pdspi-config/selectors")

    assert resp.status_code == 200
    assert resp.json() == config["selectors"]
    

def test_get_config():
    resp = requests.get("http://localhost:8080/v1/plugin/pdspi-config/config")

    assert resp.status_code == 200
    arr = resp.json()
    assert len(arr) == 3
    for a in arr:
        assert "pluginType" in a
        assert "pluginSelectors" in a
        assert "piid" in a
        # assert "pluginTypeTitle" in a
        # assert "title" in a

def test_get_config_piid():
    resp = requests.get("http://localhost:8080/v1/plugin/pdspi-config/config/pdspi-guidance-example")

    assert resp.status_code == 200
    a = resp.json()

    assert "pluginType" in a
    assert "pluginSelectors" in a
    assert "piid" in a
    # assert "pluginTypeTitle" in a
    # assert "title" in a

    resp = requests.get("http://localhost:8080/v1/plugin/pdspi-config/config/pdspi-mapper-example")

    assert resp.status_code == 200
    a = resp.json()
    
    assert "pluginType" in a
    assert "pluginSelectors" in a
    assert "piid" in a
    # assert "pluginTypeTitle" in a
    # assert "title" in a


    resp = requests.get("http://localhost:8080/v1/plugin/pdspi-config/config/pdspi-fhir-example")

    assert resp.status_code == 200
    a = resp.json()

    assert "pluginType" in a
    assert "pluginSelectors" in a
    assert "piid" in a
    # assert "pluginTypeTitle" in a
    # assert "title" in a

synthetic_ptid = "smart-7321938"

def test_get_Patient_ptid():
    resp = requests.get(f"http://localhost:8080/v1/plugin/pdspi-fhir-example/Patient/{synthetic_ptid}")

    assert resp.status_code == 200
    a = resp.json()

    assert "id" in a
    assert a["id"] == synthetic_ptid

def test_get_Observation_ptid():
    resp = requests.get(f"http://localhost:8080/v1/plugin/pdspi-fhir-example/Observation?patient={synthetic_ptid}")

    assert resp.status_code == 200
    a = resp.json()

    assert "resourceType" in a
    assert a["resourceType"] == "Bundle"
    for entry in a["entry"]:
        assert "resource" in entry
        resource = entry["resource"]
        assert resource["resoureType"] == "Observation"
        assert resource["subject"]["reference"] == f"Patient/{synthetic_ptid}"
        
def test_get_Condition_ptid():
    resp = requests.get(f"http://localhost:8080/v1/plugin/pdspi-fhir-example/Condition?patient={synthetic_ptid}")

    assert resp.status_code == 200
    a = resp.json()

    assert "resourceType" in a
    assert a["resourceType"] == "Bundle"
    for entry in a["entry"]:
        assert "resource" in entry
        resource = entry["resource"]
        assert resource["resoureType"] == "Condition"
        assert resource["subject"]["reference"] == f"Patient/{synthetic_ptid}"

