import csv
import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

with open('bills.csv', "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for line in reader:
        con.execute('INSERT INTO bills(number, title, date_introduced, date_updated, origin, type, congress) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    [int(line['number']),
                    line['title'],
                    line['introducedDate'],
                    line['updateDate'],
                    line['originChamber'],
                    line['type'],
                    line['congress'],]
                    )

con.commit()
