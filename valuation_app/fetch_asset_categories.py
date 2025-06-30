"""Utilities to download effective life tables from the ATO web site."""

import json
import os
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

URL = "https://www.ato.gov.au/law/view/document?LocID=%22TXR%2FTR20213%2FNAT%2FATO%2FatTABLE-ELECTRICITY%22&PiT=99991231235958#TABLE-ELECTRICITY"


def fetch_asset_categories(url: str = URL) -> List[Dict[str, str]]:
    """Return a flat list of asset categories with industry info.

    Each item in the returned list contains ``industry``, ``sub_industry``,
    ``broader_asset_category``, ``asset_category`` and ``life`` keys.
    """

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    records: List[Dict[str, str]] = []
    current_industry: Optional[str] = None
    current_sub_industry: Optional[str] = None

    current_broader: Optional[str] = None


    for element in soup.find_all(["h3", "h4", "table"]):
        if element.name == "h3":
            current_industry = element.get_text(strip=True)
            current_sub_industry = None
        elif element.name == "h4":
            current_sub_industry = element.get_text(strip=True)
        elif element.name == "table" and current_industry:
            rows = element.find_all("tr")

            # The first row may contain the sub-industry name merged across
            # multiple columns. Detect this by checking for a single cell or a
            # cell with a ``colspan`` attribute greater than one.
            data_start = 1
            if rows:
                first_cells = rows[0].find_all(["td", "th"])
                if len(first_cells) == 1 or any(int(c.get("colspan", 1)) > 1 for c in first_cells):
                    current_sub_industry = rows[0].get_text(strip=True)
                    # Skip the first two rows (sub-industry heading and column headings)
                    data_start = 2
            current_broader = current_sub_industry

            for row in rows[data_start:]:
                cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
                if not cols:
                    continue

                heading = len(cols) == 1 or all(not c for c in cols[1:])
                first_text = cols[0]

                if heading and first_text.endswith(":"):
                    current_broader = first_text.rstrip(":").strip()
                    continue


                if len(cols) >= 2:
                    records.append({
                        "industry": current_industry,
                        "sub_industry": current_sub_industry or "",
                        "broader_asset_category": current_broader or (current_sub_industry or ""),
                        "asset_category": first_text,
                        "life": cols[-3],
                    })
    return records


def save_to_json(data: List[Dict[str, str]]) -> None:
    """Save the records to ``ato_asset_categories.json`` in this package."""
    output_path = os.path.join(os.path.dirname(__file__), "Electricity_gas_waste_water_asset_categories.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    categories = fetch_asset_categories()
    save_to_json(categories)
