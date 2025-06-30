# jeihaan.github.io

This repository contains sample web assets and a small Flask application for a tangible asset valuation demo. The `valuation_app` folder provides a simple interface to upload a Fixed Asset Register and calculate each asset's age based on a valuation date.

## Running the Valuation App

1. Install dependencies:
   ```bash
   pip install -r valuation_app/requirements.txt
   ```
2. Start the server:
   ```bash
   python valuation_app/mainapp.py
   ```
3. Open your browser at `http://localhost:5000` and upload your FAR file.

The application expects the register to include an **Asset acquisition date** column and will add an **Asset Age (years)** column to the exported file.
