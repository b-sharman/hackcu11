from flask import Flask
from flask import jsonify, request
import requests
import sqlite3
from dotenv import load_dotenv
import os
import pickle
import pandas as pd
import datetime

filename = './model/model.pkl'
with open(filename, 'rb') as f:
    model = pickle.load(f)
#print(type(model))

app = Flask(__name__)
load_dotenv(".env.local")

TYPE_MAP = {
    'HCONRES': 'house-concurrent-resolution',
    'HJRES': 'house-joint-resolution',
    'HR': 'house-bill',
    'HRES': 'house-resolution',
    'S': 'senate-bill',
    'SCONRES': 'senate-concurrent-resolution',
    'SJRES': 'senate-joint-resolution',
    'SRES': 'senate-resolution',
}

def get_url(bill):
    return f"https://www.congress.gov/bill/{bill['congress']}th-congress/{TYPE_MAP[bill['type']]}/{bill['number']}"

def get_subjects(bill):
    response = requests.get(f"https://api.congress.gov/v3/bill/{bill['congress']}/{bill['type'].lower()}/{bill['number']}/subjects?api_key={os.getenv('VITE_API_KEY')}&format=json&limit=250").json()
    return [subject['name'] for subject in response['subjects']['legislativeSubjects']]

def get_summary(bill):
    response = requests.get(f"https://api.congress.gov/v3/bill/{bill['congress']}/{bill['type'].lower()}/{bill['number']}/summaries?api_key={os.getenv('VITE_API_KEY')}&format=json&limit=1").json()
    try:
        return {'exists': True, 'summary': response['summaries'][0]['text']}
    except:
        return {'exists': False}

def get_actions(bill):
    actions = requests.get(f"https://api.congress.gov/v3/bill/{bill['congress']}/{bill['type'].lower()}/{bill['number']}/actions?api_key={os.getenv('VITE_API_KEY')}&format=json").json()
    return [action for action in actions["actions"] if not ('actionCode' in action and action['actionCode'] == "Intro-H")]

def map_to_dict(bill):
    return {
        'id': bill[0],
        'number': bill[1],
        'title': bill[2],
        'date_introduced': bill[3],
        'date_updated': bill[4],
        'origin': bill[5],
        'type': bill[6],
        'congress': bill[7],
    }

@app.route("/search")
def search():
    query = request.args.get('q')
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    bills = [map_to_dict(bill)for bill in cur.execute(r"SELECT * FROM bills WHERE title LIKE ? ORDER BY congress DESC LIMIT 10", [f"%{query}%"]).fetchall()]
    res = jsonify([bill | {
        'url': get_url(bill)
    } for bill in bills])
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

@app.route('/summary')
def summary():
    id = request.args.get('id')
    db = sqlite3.connect('database.db')
    cur = db.cursor()

    bill = map_to_dict(cur.execute("SELECT * FROM bills WHERE id = ?", [id]).fetchone())
    
    summary = get_summary(bill)
    status = 200 if summary['exists'] else 404
    res = jsonify(summary)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res, status

def map_to_df_dict(bill):
    update = pd.to_datetime(bill[4].split('T')[0])
    introduced = pd.to_datetime(bill[3])

    duration = (update - introduced).days

    return [
        float(bill[1]),
        float(bill[7]),
        float(duration),
        float(bill[6] == 'HCONRES'),
        float(bill[6] == 'HJRES'),
        float(bill[6] == 'HR'),
        float(bill[6] == 'HRES'),
        float(bill[6] == 'S'),
        float(bill[6] == 'SCONRES'),
        float(bill[6] == 'SJRES'),
        float(bill[6] == 'SRES'),
        float(bill[5] == 'House'),
        float(bill[5] == 'Senate'),
    ]

def get_prediction(bill):
    prediction = model.predict([bill])
    probability = model.predict_proba([bill])

    if prediction[0] == 0:
        prediction = 'No'
    else:
        prediction = 'Yes'

    return {'prediction': prediction, 'probability': probability[0][1]}

@app.route('/predict')
def predict():
    id = request.args.get('id')
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    bill = map_to_df_dict(cur.execute("SELECT * FROM bills WHERE id = ?", [id]).fetchone())
    
    res = jsonify(get_prediction(bill))
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res


@app.route("/bill")
def bill():
    id = request.args.get('id')
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    bill_tuple = cur.execute("SELECT * FROM bills WHERE id = ?", [id]).fetchone()
    bill = map_to_dict(bill_tuple)
    bill_df = map_to_df_dict(bill_tuple)
    prediction = get_prediction(bill_df);

    bill_data = requests.get(f"https://api.congress.gov/v3/bill/{bill['congress']}/{bill['type'].lower()}/{bill['number']}?api_key={os.getenv('VITE_API_KEY')}&format=json").json()

    res = jsonify(bill | {
        'prediction': prediction,
        'subjects': get_subjects(bill),
        'summary': get_summary(bill),
        'actions': get_actions(bill),
        'url': get_url(bill),
        'data': bill_data,
    })
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

