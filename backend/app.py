from flask import Flask
from flask import jsonify, request
import requests
import sqlite3
from dotenv import load_dotenv
import os
import pickle
import pandas as pd
import random

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

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
    return response['summaries'][0]['text']

def get_actions(bill):
    return requests.get(f"https://api.congress.gov/v3/bill/{bill['congress']}/{bill['type'].lower()}/{bill['number']}/actions?api_key={os.getenv('VITE_API_KEY')}&format=json").json()

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
    try:
        res = jsonify({'exists': True, 'summary': get_summary(bill)})
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res, 200
    except:
        res = jsonify({'exists': False})
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res, 404

@app.route('/predict')
def predict():
    df = pd.read_csv('newest_bills.csv')
    rand = random.randint(0, len(df))
    bill = df.iloc[rand]
    prediction = model.predict([bill])
    print(prediction)

@app.route("/bill")
def bill():
    id = request.args.get('id')
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    bill = map_to_dict(cur.execute("SELECT * FROM bills WHERE id = ?", [id]).fetchone())

    bill_data = requests.get(f"https://api.congress.gov/v3/bill/{bill['congress']}/{bill['type'].lower()}/{bill['number']}?api_key={os.getenv('VITE_API_KEY')}&format=json").json()

    res = jsonify(bill | {
        'subjects': get_subjects(bill),
        'summary': get_summary(bill),
        'actions': get_actions(bill),
        'data': bill_data,
    })
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

