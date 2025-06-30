"""Fetch PPI data and structure from the ABS API and save to JSON files."""

import json
import os
from typing import Any, Dict

import requests

STRUCTURE_URL = "https://data.api.abs.gov.au/rest/dataflow/ABS/PPI/?references=all"

DATA_URL = (
    "https://data.api.abs.gov.au/rest/data/ABS,PPI,/"
    "1.7011001+7013001+7013002+7013003+7013004+7013005+7013006+7013007+7013010+"
    "7015231+7015232+7015233+7015234+7015240+7015241+7015243+7015244+7015245+"
    "7015246+7015247+7015248+7015250+7015252+7015255+7015256+7015257+7015258+"
    "7015259+7015262+7015263+7071001+7081001+7101001+7111001+7121001+7131001+"
    "7141001+7151001+7161001+7171001+7181001+7191001+7222001+7222002+8102176+"
    "8102177+8102191+8102192+8102194+8102195+8102226+8102227+8102255+8102258+"
    "8102294+8102308+8102309+8102310+8102329+8102336+8102344+8102352+8102359+"
    "8102366+8102374+8102381+8102390+8102398+8102405+8102412+8102426+8102438+"
    "8102446+8102453+8102460+8102467+8102475+8102482+8102489+8102496+8102503+"
    "8102510+8102544+8102560+8102576+8102591+8102825+8104018+8104034+8104049+"
    "8104096+8104097+8104098+8104099+8104100+8104101+8104102+8104103+8104104+"
    "8104105+8104601+8104602+8104603+8104604+8104605+8104606+8104607+8104608+"
    "8104609+8104610+8104611+8104612+8104613+8104614+8104615+8104616+8104617+"
    "8104618+8104619+8104620+8104621+8104622+8104623+8104624+8104625+8104626+"
    "8104627+8104628+8104629+8104630+8104631+8104632+8104633+8104634+8104635+"
    "8104636+8104637+8104638+8104639+8104640+8104641+8104642+8104643+8104644+"
    "8104645+8104646+8104647+8104648+8104649+8104650+8104651+8104652+8104653+"
    "8104654+8104655+8104656+8104657+8104658+8104659+8105064+8127546+8127772+"
    "8127969+8128375+8132989+8132999+8133017+8133201+8133232+8133257+8133344+"
    "8133366+8133475+8133486+8133487+8133630+8133631+8133665+8133686+8133730+"
    "8133842+8133866+8133887+8133903+8133910+8133916+8133922+8136045+8195697+"
    "T11+T13+T14.INPUT.Q?endPeriod=2025-Q1&dimensionAtObservation=AllDimensions"
)


def _fetch_json(url: str) -> Dict[str, Any]:
    """Retrieve JSON data from the given ``url``."""
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def fetch_structure(url: str = STRUCTURE_URL) -> Dict[str, Any]:
    """Fetch the dataset structure from the ABS API."""
    return _fetch_json(url)


def fetch_data(url: str = DATA_URL) -> Dict[str, Any]:
    """Fetch the PPI data from the ABS API."""
    return _fetch_json(url)


def save_json(data: Dict[str, Any], filename: str) -> None:
    """Save ``data`` to ``filename`` inside this package."""
    output_path = os.path.join(os.path.dirname(__file__), filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    structure = fetch_structure()
    save_json(structure, "abs_ppi_structure.json")

    data = fetch_data()
    save_json(data, "abs_ppi_data.json")
