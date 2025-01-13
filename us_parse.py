import sqlite3
import http.client
import json
from urllib.parse import quote  # For URL encoding

# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 

load_dotenv()

# List of all locations
locations = ["alabama",
    "louisiana", "kentucky", "oregon", "oklahoma", "connecticut", "utah", "nevada",
    "arkansas", "kansas", "mississippi", "new mexico", "iowa", "west virginia",
    "nebraska", "idaho", "hawaii", "maine", "new hampshire", "montana", "rhode island",
    "delaware", "south dakota", "north dakota", "alaska", "vermont", "wyoming",
    "district of columbia", "puerto rico", "guam", "us virgin islands", "american samoa",
    "northern mariana islands"
]

# Connect to SQLite (creates the database if it doesn't exist)
conn = sqlite3.connect('sd_salaries_us.db')  # Replace with your desired database name
cursor = conn.cursor()

# Create the table if it doesn't already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS SDUSsalaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    job_title TEXT,
    min_salary REAL,
    max_salary REAL,
    median_salary REAL,
    salary_period TEXT,
    salary_currency TEXT
);
""")

# Iterate over locations and fetch data
for location in locations:
    encoded_location = quote(location)  # Encode the location for URL
    conn_http = http.client.HTTPSConnection(os.getenv("API_HOST"))

    headers = {
        'x-rapidapi-key': os.getenv("API_KEY"),
        'x-rapidapi-host': os.getenv("API_HOST")
    }

    try:
        # Make the API request
        conn_http.request("GET", f"/job-salary?job_title=software%20developer&location={encoded_location}&location_type=ANY&years_of_experience=ALL", headers=headers)
        res = conn_http.getresponse()
        data = res.read()

        # Parse JSON data
        parsed_data = json.loads(data.decode("utf-8"))

        # Insert data into the table
        for item in parsed_data.get('data', []):
            job_title = item['job_title']
            min_salary = item['min_salary']
            max_salary = item['max_salary']
            median_salary = item['median_salary']
            salary_period = item['salary_period']
            salary_currency = item['salary_currency']

            cursor.execute('''INSERT INTO SDUSsalaries (location, job_title, min_salary, max_salary, median_salary, salary_period, salary_currency)
                              VALUES (?, ?, ?, ?, ?, ?, ?)''', (
                location, job_title, min_salary, max_salary, median_salary, salary_period, salary_currency
            ))

        conn.commit()
    except Exception as e:
        print(f"Error for location '{location}': {e}")

# Verify data
cursor.execute("SELECT * FROM SDUSsalaries")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
