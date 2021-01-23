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

    def check_if_exists(self, barcode: int):
        # Connect to the database and create the cursor
        conn = self.sqlite3.connect('database.db')
        c = conn.cursor() # Database cursor
        print('Successfully connected to database.')
        print('Querying whether the following barcode exists - ' + str(barcode))
        c.execute('SELECT * from fooddata where barcode=?', (barcode,))
        # If the record does not exist with that barcode, return false
        if not c.fetchall():
            conn.close()
            print('SQLite connection closed')
            return False
        else:
            conn.close()
            print('SQLite connection closed')
            return True

    def remove_item(self, barcode: int):
        try:
            # Connect to the database and create the cursor
            conn = self.sqlite3.connect('database.db')
            c = conn.cursor() # Database cursor
            print('Successfully connected to database.')
            c.execute('DELETE FROM fooddata WHERE barcode=?', (barcode,))
            conn.commit()
            print('Item with barcode ' + str(barcode) + ' removed successfully')
            c.close()
        except self.sqlite3.Error as error:
           print('Falied to remove item', error)
        finally:
            if conn:
                conn.close()
                print('SQLite connection closed')

    def retrieve_item(self, barcode: int):
        retrieved_item = FoodData(0, '', '', '', 0, '')
        try:
            # Check whether the item exists first
            if not self.check_if_exists(barcode):
                return False
            # Get the entry if the item exists
            conn = self.sqlite3.connect('database.db')
            c = conn.cursor() # Database cursor
            print('Getting the following entry - ' + str(barcode))
            c.execute('SELECT * from fooddata where barcode=?', (barcode,))
            record = c.fetchall()
            print('Total rows fetched = ', len(record))
            # Create a blank FoodData class to store the result
            
            for row in record:
                retrieved_item.barcode = barcode
                retrieved_item.date = datetime.datetime.strptime(row[1], "%d/%m/%Y, %H:%M")
                retrieved_item.name = row[2]
                retrieved_item.quantity = row[3]
                retrieved_item.amount = row[4]
                retrieved_item.off_url = row[5]
        except self.sqlite3.Error as error:
           print('Falied to remove item', error)
        finally:
            if conn:
                conn.close()
                print('SQLite connection closed')
            if retrieved_item:
                return retrieved_item
        
