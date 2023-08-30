import sqlite3 
import sys
import os 

CREATE_TABLES_PATH = 'scripts/create.sql'
INSERT_BASIC_PATH = 'scripts/insert.sql'
INSERT_REVIEWS_PATH = 'scripts/insert_reviews.sql'

DATABASE_PATH = 'data/review.db'

def create_database():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
    except:
        print('\'data\' folder was not found')
        
    cursor = conn.cursor()
    cursor.executescript(get_script(CREATE_TABLES_PATH))
    conn.commit()
    print("Tables Created")

    cursor.executescript(get_script(INSERT_BASIC_PATH))
    conn.commit()
    print("Basic data inserted")

    cursor.executescript(get_script(INSERT_REVIEWS_PATH))
    conn.commit()
    print("Reviews inserted")

    conn.close()

def get_script(file_path: str):
    if (not os.path.isfile(file_path)):
        print(f'{file_path} does not exist')
        exit()

    with open(file_path, 'r') as file:
        script = file.read()

    return script



if __name__ in '__main__':
    if (os.path.isfile(DATABASE_PATH)):
        os.remove(DATABASE_PATH)

    create_database()