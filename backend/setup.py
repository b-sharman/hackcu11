import sqlite3

db = sqlite3.connect('database.db')

db.execute(
    "CREATE TABLE IF NOT EXISTS bills(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, number INT NOT NULL, title VARCHAR(255) NOT NULL, date_introduced VARCHAR(255) NOT NULL, date_updated VARCHAR(255) NOT NULL, origin VARCHAR(255) NOT NULL, type VARCHAR(255) NOT NULL, congress INT NOT NULL)"
    )
