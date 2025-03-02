from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)

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
    return [bill | {'url': get_url(bill)} for bill in bills]
    