from flask import Flask, render_template, request, redirect, jsonify
import os
import csv
import uuid

# Import the process_data function from model.py
from model import process_data

app = Flask(__name__)

# Ensure the static directory and data.csv file exist with the new headers
directory = './static'
path = os.path.join(directory, 'data.csv')

if not os.path.exists(directory):
    os.makedirs(directory)

# Initialize CSV file with headers if it does not exist
if not os.path.exists(path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'First Name', 'Last Name', 'Gender', 'Temperature', 'Heart Rate', 'Respiratory Rate', 'White Blood Cells', 'Blood Group', 'Your Concerns', 'Sepsis'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['Lname']
        gender = request.form['gender']
        temperature = request.form['temperature']
        heart_rate = request.form['heart-rate']
        respiratory_rate = request.form['respiratory-rate']
        wbc = request.form['wcb']
        blood_group = request.form['blood-group']
        concerns = request.form['You Concerns']

        # Process the data using the model to check for sepsis
        form_data = {
            'fname': first_name,
            'Lname': last_name,
            'gender': gender,
            'temperature': temperature,
            'heart-rate': heart_rate,
            'respiratory-rate': respiratory_rate,
            'wcb': wbc,
            'blood-group': blood_group,
            'You Concerns': concerns
        }
        sepsis_status = process_data(form_data)
        
        # Generate a new ID (UUID in this case)
        record_id = str(uuid.uuid4())

        # Save the data to data.csv
        with open(path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([record_id, first_name, last_name, gender, temperature, heart_rate, respiratory_rate, wbc, blood_group, concerns, sepsis_status])

        # Redirect to the home page
        # return redirect('/')
        return jsonify({'sepsis_status': sepsis_status})

# Path to your CSV file
CSV_FILE_PATH = './static/data.csv'

def delete_record_from_csv(csv_file, record_id):
    """Deletes a record from a CSV file based on the ID.

    Args:
        csv_file (str): The path to the CSV file.
        record_id (str): The ID of the record to delete.
    """
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        header = rows[0]

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in rows[1:]:  # Skip header
            if row[0] != record_id:
                writer.writerow(row)


@app.route('/delete-record', methods=['POST'])
def delete_record():
    data = request.get_json()
    record_id = data.get('id')

    if not record_id:
        return jsonify({'success': False, 'message': 'No ID provided'})

    try:
        delete_record_from_csv(CSV_FILE_PATH, record_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
