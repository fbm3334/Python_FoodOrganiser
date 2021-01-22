# Check whether the database.db file exists - if it does not, then create it


import sqlite3
conn = sqlite3.connect('database.db')