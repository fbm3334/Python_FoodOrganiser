from dataclasses import dataclass
import datetime

@dataclass
class FoodData:
    barcode: int
    date: datetime
    name: str
    quantity: str
    amount: int = 1
    off_url: str = ''

class FoodDatabase:
    import sqlite3

    def __init__(self):
        # Initially open database.db to check that it exists
        f = open('database.db', 'a') # Append
        f.close() # Close straight away

        # Import sqlite3 to perform database operations
        conn = self.sqlite3.connect('database.db')
        c = conn.cursor() # Database cursor

        # Check whether the file is empty
        import os
        if os.stat('database.db').st_size == 0:
            print('File is empty.')
            # Initialise the table
            c.execute('''CREATE TABLE fooddata
                        (barcode integer PRIMARY KEY, date text, name text, quantity text, amount real, url text)''')
            conn.commit()
            print('Created the SQL table.')
        else:
            print('Database file already exists.')
        
        conn.close() # Close the database connection when done

    def add_item(self, item: FoodData):
        try:
            # Connect to the database and create the cursor
            conn = self.sqlite3.connect('database.db')
            c = conn.cursor() # Database cursor
            print('Successfully connected to database.')
            print('Adding the following data - ' + str(item))
            insert_param = ('''INSERT INTO fooddata
                        (barcode, date, name, quantity, amount, url)
                        VALUES (?, ?, ?, ?, ?, ?);''')
            # Need to convert date/time into a string
            date_string = item.date.strftime("%d/%m/%Y, %H:%M")
            data_tuple = (item.barcode, date_string, item.name, item.quantity, item.amount, item.off_url)
            c.execute(insert_param, data_tuple)
            conn.commit()
            print('Item added successfully')
            c.close()
        except self.sqlite3.Error as error:
            print('Failed to insert the item into the SQLite table', error)
        finally:
            if conn:
                conn.close()
                print('SQLite connection closed')

