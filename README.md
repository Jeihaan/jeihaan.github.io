# jeihaan.github.io

This repository contains sample web assets and a small Flask application for a tangible asset valuation demo. The `valuation_app` folder provides a simple interface to upload a Fixed Asset Register and calculate each asset's age based on a valuation date.

## Cloning the Repository

Clone the repository and navigate into its directory:

```bash
git clone https://github.com/jeihaan/jeihaan.github.io.git
cd jeihaan.github.io
```


## Running the Valuation App

1. Install dependencies:
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use "venv\Scripts\activate"
   ```
2. Install dependencies inside the virtual environment:
   ```bash
   pip install -r valuation_app/requirements.txt
   ```
2. Start the server:
3. Start the server. Use the `-m` flag so Python treats the application as a
   package (this avoids import issues):
   ```bash
   python valuation_app/mainapp.py
   python -m valuation_app.mainapp
   ```
3. Open your browser at `http://localhost:5000` and upload your FAR file.
4. Open your browser at `http://localhost:5000` and upload your FAR file.

The application expects the register to include an **Asset acquisition date** column and will add an **Asset Age (years)** column to the exported file.

## Fetching ATO Asset Categories

The repository includes a helper script to download effective life tables from
the ATO website. Running it will create `valuation_app/ato_asset_categories.json`
containing a list of records with the following keys:

* `industry`
* `sub_industry`
* `broader_asset_category`
* `asset_category`
* `life`

Sub-industry names are derived from the first row of each table in the ATO
document. When a table contains no broader category headings, the
`broader_asset_category` value repeats the sub-industry name.
* `asset_category`
* `life`

```bash
python valuation_app/fetch_asset_categories.py
```


## Fetching ABS PPI Data

The repository also includes a script to download the structure and data for the ABS Producer Price Index dataset. Running it will create `valuation_app/abs_ppi_structure.json` and `valuation_app/abs_ppi_data.json`.

```bash
python valuation_app/fetch_ppi_data.py
```

