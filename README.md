# jeihaan.github.io

This repository contains sample web assets and a small Flask application for a tangible asset valuation demo. The `valuation_app` folder provides a simple interface to upload a Fixed Asset Register and calculate each asset's age based on a valuation date.

## Cloning the Repository

Clone the repository and navigate into its directory:

```bash
git clone https://github.com/jeihaan/jeihaan.github.io.git
cd jeihaan.github.io
```


## Running the Valuation App

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use "venv\Scripts\activate"
   ```
2. Install dependencies inside the virtual environment:
   ```bash
   pip install -r valuation_app/requirements.txt
   ```
3. Start the server:
   ```bash
   python valuation_app/mainapp.py
   ```
4. Open your browser at `http://localhost:5000` and upload your FAR file.

The application expects the register to include an **Asset acquisition date** column and will add an **Asset Age (years)** column to the exported file.

## Fetching ATO Asset Categories

The repository includes a helper script to download the industry asset
categories and their NUL (normal useful life) values from the ATO website.
Run the script and it will create `valuation_app/ato_asset_categories.json`:

```bash
python valuation_app/fetch_asset_categories.py
```
