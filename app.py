from flask import Flask, render_template, request, jsonify
import os
from csv import writer
from chatbot import get_chat_response

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
        writer_object = writer(file)
        writer_object.writerow(['First Name', 'Last Name', 'Gender', 'Temperature', 'Heart Rate', 'Respiratory Rate', 'White Blood Cells', 'Blood Group', 'Your Concerns', 'Sepsis'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if user_message:
        response = get_chat_response(user_message)
        return jsonify({'response': response})
    return jsonify({'response': 'No message received'})

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

        # Read the existing data
        if os.path.exists(path):
            with open(path, 'r') as file:
                existing_data = list(file.readlines())
        else:
            existing_data = []

        # Prepare the new row of data
        new_row = f"{first_name},{last_name},{gender},{temperature},{heart_rate},{respiratory_rate},{wbc},{blood_group},{concerns},{sepsis_status}\n"

        # Insert the new row at the top of the data
        updated_data = [existing_data[0]] + [new_row] + existing_data[1:] if existing_data else [new_row]

        # Write the updated data back to the CSV file
        with open(path, 'w', newline='\n') as file:
            file.writelines(updated_data)

        return jsonify({'sepsis_status': sepsis_status})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
