import sqlite3

def select_from_table(db_name, table_name):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Execute the SELECT query
    cursor.execute(f"SELECT * FROM {table_name}")

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    return rows

if __name__ == "__main__":
    db_name = 'sd_salaries_us.db'
    table_name = 'SDUSsalaries'
    rows = select_from_table(db_name, table_name)
    for row in rows:
        print(row)