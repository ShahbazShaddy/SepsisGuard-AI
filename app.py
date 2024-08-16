from flask import Flask, render_template, request, redirect
import csv
import os

# Import the process_data function from model.py
from model import process_data

app = Flask(__name__)

# Ensure the data.csv file exists with the new headers
if not os.path.exists('data.csv'):
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['First Name', 'Last Name', 'Gender', 'Temperature', 'Heart Rate', 'Respiratory Rate', 'White Blood Cells', 'Blood Group', 'Your Concerns'])

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

        # Save the data to data.csv
        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([first_name, last_name, gender, temperature, heart_rate, respiratory_rate, wbc, blood_group, concerns])

        # Process the data using the model
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
        process_data(form_data)

        # Redirect to the home page
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
