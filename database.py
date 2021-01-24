from dataclasses import dataclass
import datetime

@dataclass
class FoodData:
    barcode: int
    date: datetime
    name: str
    quantity: str
    amount: float = 1.0
    img_url: str = ''

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
        conn = self.sqlite3.connect('database.db')
        c = conn.cursor() # Database cursor
        try:
            # Connect to the database and create the cursor
            
            print('Successfully connected to database.')
            print('Adding the following data - ' + str(item))
            insert_param = ('''INSERT INTO fooddata
                        (barcode, date, name, quantity, amount, url)
                        VALUES (?, ?, ?, ?, ?, ?);''')
            # Need to convert date/time into a string
            date_string = item.date.strftime("%Y-%m-%d %H:%M:%S")
            print(type(date_string))
            data_tuple = (item.barcode, date_string, item.name, item.quantity, item.amount, item.img_url)
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
        conn = self.sqlite3.connect('database.db')
        # Check whether the item exists first
        if not self.check_if_exists(barcode):
            return False
        # Get the entry if the item exists
        
        c = conn.cursor() # Database cursor
        print('Getting the following entry - ' + str(barcode))
        c.execute('SELECT * from fooddata where barcode=?', (barcode,))
        record = c.fetchall()
        print('Total rows fetched = ', len(record))
        # Create a blank FoodData class to store the result
        retrieved_item.barcode = barcode
        extracted_tuple = record[0]
        print(extracted_tuple)
        retrieved_item.date = datetime.datetime.strptime(extracted_tuple[1], "%Y-%m-%d %H:%M:%S")
        retrieved_item.name = extracted_tuple[2]
        retrieved_item.quantity = extracted_tuple[3]
        retrieved_item.amount = extracted_tuple[4]
        retrieved_item.img_url = extracted_tuple[5]
        print("Retrieved...", retrieved_item)
        if conn:
            conn.close()
            print('SQLite connection closed')
        if retrieved_item:
            return retrieved_item
        
    def update_amount(self, barcode: int, amount_change: float):
        # Retrieve the item
        retrieved_item = FoodData(0, '', '', '', 0, '')
        retrieved_item = self.retrieve_item(barcode)
        # Update the amount
        new_amount = retrieved_item.amount + amount_change
        retrieved_item.amount = new_amount
        # Delete the old entry
        self.remove_item(barcode)
        # Add the new entry
        # Only add it if the quantity is greater than 0, else only remove
        if retrieved_item.amount > 0:
            self.add_item(retrieved_item)

    def get_all_items(self):
        # Query to retrieve all items from database
        conn = self.sqlite3.connect('database.db')
        c = conn.cursor() # Database cursor
        print('Getting all entries:')
        c.execute('SELECT * from fooddata')
        record = c.fetchall()
        if not record:
            conn.close()
            print('SQLite connection closed')
            return False
        # Create an array of FoodData classes
        items = []
        for row in record:
            retrieved_item = FoodData(0, '', '', '', 0, '')
            retrieved_item.barcode = int(row[0])
            retrieved_item.date = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            retrieved_item.name = row[2]
            retrieved_item.quantity = row[3]
            retrieved_item.amount = row[4]
            retrieved_item.img_url = row[5]
            items.append(retrieved_item)

        if conn:
            conn.close()
            print('SQLite connection closed')

        return items

    def save_items_csv(self, items_array):
        import csv
        from os import path, remove
        if path.exists('food_csv.csv'):
            remove('food_csv.csv')
        
        f = open('food_csv.csv', 'a') # Append

        linewriter = csv.writer(f, dialect='excel')
        linewriter.writerow(['Barcode', 'Date added', 'Product name', 'Product quantity', 'Amount remaining', 'Image URL'])
        for item in items_array:
            linewriter.writerow([item.barcode, item.date, item.name, item.quantity, item.amount, item.img_url])
        
        f.close()
        