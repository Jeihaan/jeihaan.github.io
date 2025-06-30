from flask import Flask, render_template, request, send_file
import os
import pandas as pd
try:
    # When executed as a package (e.g. ``python -m valuation_app.mainapp``)
    from .valuations import load_far, compute_asset_age
except ImportError:  # Fallback when running this file directly
    from valuations import load_far, compute_asset_age

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        valuation_date = request.form.get('valuation_date')
        industry = request.form.get('industry')
        file = request.files.get('far_file')
        if file and valuation_date:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            df = load_far(file_path)
            df = compute_asset_age(df, valuation_date)
            result_path = os.path.join(UPLOAD_FOLDER, f"result_{file.filename}")
            df.to_excel(result_path, index=False)
            return send_file(result_path, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
