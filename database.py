class FoodDatabase:
    import sqlite3

    def __init__(self):
        # Initially open database.db to check that it exists
        f = open('database.db', 'a') # Append
        f.close() # Close straight away

        # Import sqlite3 to perform database operations
        import sqlite3
        conn = sqlite3.connect('database.db')
        c = conn.cursor() # Database cursor

        # Check whether the file is empty
        import os
        if os.stat('database.db').st_size == 0:
            print('File is empty.')
            # Initialise the table
            c.execute('''CREATE TABLE fooddata
                        (date text, name text, quantity text, amount real, url text)''')
            conn.commit()
            print('Created the SQL table.')
        else:
            print('Database file already exists.')
        
        conn.close() # Close the database connection when done
        
