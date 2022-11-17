import io
from flask import Flask, render_template, request
import csv

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index_page():
    return render_template('index.html')

@app.post("/response")
def response_page():
    inputs = []
    prediction = ''

    input_file = request.files.get('input_file', None)
    has_input_file = input_file is not None and input_file.content_type == 'text/csv'

    if has_input_file:
        input_file = request.files.get('input_file')
        input_file.stream.seek(0)
        input_data = io.StringIO(input_file.stream.read().decode("UTF8"))
        csv_reader = csv.DictReader(input_data, delimiter=',', quotechar='"')
        for row in csv_reader:
            inputs = [
                row['blood_pressure'],
                row['fever'],
                row['diabetes'],
                row['vomit']
            ]

    else:
        data = request.form
        inputs = [
            data.get('blood_pressure'),
            data.get('fever'),
            data.get('diabetes'),
            data.get('vomit')
        ]

    classifier = request.form.get('classifier')

    return render_template('response.html', 
        inputs=inputs,
        classifier=classifier,
        prediction=prediction
    )