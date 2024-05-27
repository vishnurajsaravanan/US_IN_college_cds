import sqlite3


# Store everything in a database SQL
def store_db(college_name, file_name, url):
    conn = sqlite3.connect('college_cds.db')
    curr = conn.cursor()
    curr.execute('''
        CREATE TABLE IF NOT EXISTS search_result (
            college_name VARCHAR(100), 
            file_name VARCHAR(100), 
            url VARCHAR(100)
        )
    ''')
    # insert data into a table
    curr.execute("INSERT INTO search_result (college_name, file_name, url) VALUES (?,?,?)", 
                    (college_name, file_name, url))    
    conn.commit()
    conn.close()