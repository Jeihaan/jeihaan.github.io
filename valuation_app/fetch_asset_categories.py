import json
import os
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

URL = "https://www.ato.gov.au/law/view/document?DocID=TXR%2FTR20213%2FNAT%2FATO%2F00003"


def fetch_asset_categories() -> Dict[str, List[Dict[str, str]]]:
    """Fetch asset categories from the ATO website and structure them by industry."""
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    data: Dict[str, List[Dict[str, str]]] = {}
    current_industry: str | None = None
    for element in soup.find_all(["h3", "table"]):
        if element.name == "h3":
            current_industry = element.get_text(strip=True)
            data[current_industry] = []
        elif element.name == "table" and current_industry:
            rows = element.find_all("tr")
            for row in rows[1:]:
                cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
                if len(cols) >= 2:
                    category = cols[0]
                    nul = cols[-1]
                    data[current_industry].append({"category": category, "nul": nul})
    return data


def save_to_json(data: Dict[str, List[Dict[str, str]]]) -> None:
    """Save the data to ato_asset_categories.json in this package."""
    output_path = os.path.join(os.path.dirname(__file__), "ato_asset_categories.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    categories = fetch_asset_categories()
    save_to_json(categories)
