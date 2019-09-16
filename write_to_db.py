import sqlite3
import csv
# Connects to 'motorolaProductsClone' sqlite3 database
conn = sqlite3.connect('icomProducts.db')

# Sets cursor
cursor = conn.cursor()

def insert_into_table():
    with open('icom-accessories2.csv', 'r', encoding='utf-8') as f:
        r = csv.reader(f)
        next(f)

        for row in r:
            sku = row[0]
            name = row[1]
            desc = row[2]
            price = row[3]
            tags = row[4]
            category = row[5]

            cursor.executemany("INSERT INTO accessories values(?, ?, ?, ?, ?, ?)",
                               [
                                   (sku, name, desc, price, tags, category)
                               ])
            conn.commit()
# insert_into_table()
