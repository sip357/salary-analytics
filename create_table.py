import sqlite3

# Connect to SQLite (creates the database if it doesn't exist)
conn = sqlite3.connect('sd_salaries_us.db')  # Replace with your desired database name
cursor = conn.cursor()

# Create a table
cursor.execute(''' CREATE TABLE SDUSsalaries (
                    id INTEGER PRIMARY KEY,
                    location TEXT,
                    job_title TEXT,
                    min_salary REAL,
                    max_salary REAL,
                    median_salary REAL,
                    salary_period TEXT,
                    salary_currency TEXT
                )''')
conn.commit()