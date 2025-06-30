"""Utilities to download effective life tables from the ATO web site."""

import json
import os
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

URL = "https://www.ato.gov.au/law/view/document?DocID=TXR%2FTR20213%2FNAT%2FATO%2F00003"


def fetch_asset_categories(url: str = URL) -> List[Dict[str, str]]:
    """Return a flat list of asset categories with industry info.

    Each item in the returned list contains ``industry``, ``sub_industry``,
    ``asset_category`` and ``life`` keys.
    """

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    records: List[Dict[str, str]] = []
    current_industry: Optional[str] = None
    current_sub_industry: Optional[str] = None

    for element in soup.find_all(["h3", "h4", "table"]):
        if element.name == "h3":
            current_industry = element.get_text(strip=True)
            current_sub_industry = None
        elif element.name == "h4":
            current_sub_industry = element.get_text(strip=True)
        elif element.name == "table" and current_industry:
            rows = element.find_all("tr")
            for row in rows[1:]:
                cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
                if len(cols) >= 2:
                    records.append({
                        "industry": current_industry,
                        "sub_industry": current_sub_industry or "",
                        "asset_category": cols[0],
                        "life": cols[-1],
                    })
    return records


def save_to_json(data: List[Dict[str, str]]) -> None:
    """Save the records to ``ato_asset_categories.json`` in this package."""
    output_path = os.path.join(os.path.dirname(__file__), "ato_asset_categories.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    categories = fetch_asset_categories()
    save_to_json(categories)
