import os
import json
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import plotly.graph_objs as go
import plotly.io as pio
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)

# Quiz questions
questions = [
    "The free market is the most effective way to distribute resources.",
    "Government intervention in the economy is necessary to protect citizens.",
    "Private property rights should be protected at all costs.",
    "A strong welfare system is essential for a just society.",
    "Corporations should be subject to strict regulations.",
    "Labor unions are essential for protecting workers' rights.",
    "Taxation is a form of theft.",
    "Universal healthcare should be provided by the government.",
    "Education should be privatized.",
    "Environmental regulations are necessary to combat climate change.",
    "The government should have a strong military presence.",
    "Police powers should be limited to protect civil liberties.",
    "Freedom of speech should be absolute, with no restrictions.",
    "The death penalty is a just form of punishment for severe crimes.",
    "Gun ownership is a fundamental right that should not be infringed upon.",
    "Same-sex marriage should be legally recognized.",
    "Abortion should be legal and accessible.",
    "Immigration policies should be more restrictive.",
    "Racial and ethnic minorities should receive special protections.",
    "Religion should play a role in government policy-making."
]

# List of Albanian municipalities
municipalities = [
    "Tirana", "Durrës", "Vlorë", "Elbasan", "Shkodër", "Fier", "Kamëz", "Korçë",
    "Berat", "Lushnjë", "Kavajë", "Gjirokastër", "Sarandë", "Patos", "Lezhë",
    "Kuçovë", "Kukës", "Pogradec", "Krujë", "Burrel", "Peshkopi", "Librazhd",
    "Tepelenë", "Gramsh", "Poliçan", "Bulqizë", "Përmet", "Fushë-Krujë", "Ballsh",
    "Rrogozhinë", "Shijak", "Laç", "Mamurras", "Cërrik", "Ersekë", "Peqin",
    "Divjakë", "Selenicë", "Vorë", "Roskovec", "Bajram Curri", "Koplik", "Ura Vajgurore",
    "Himarë", "Maliq", "Delvinë", "Pukë", "Memaliaj", "Këlcyrë", "Konispol"
]

# ... (keep all the existing functions)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/demographics')
def demographics():
    return render_template('demographics.html', municipalities=municipalities)

@app.route('/submit_demographics', methods=['POST'])
def submit_demographics():
    age = request.form.get('age')
    sex = request.form.get('sex')
    education = request.form.get('education')
    city = request.form.get('city')
    
    session['demographics'] = {'age': age, 'sex': sex, 'education': education, 'city': city}
    
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', questions=questions)

# ... (keep all the existing routes and functions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
