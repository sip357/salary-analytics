import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('sd_salaries_us.db')
cursor = conn.cursor()

# Create a temporary table to store unique rows
cursor.execute('''
CREATE TABLE IF NOT EXISTS SDUSsalaries_temp AS
SELECT DISTINCT id, location, job_title, min_salary, max_salary, median_salary, salary_period, salary_currency
FROM SDUSsalaries
''')

# Drop the original table
cursor.execute('DROP TABLE SDUSsalaries')

# Rename the temporary table to the original table name
cursor.execute('ALTER TABLE SDUSsalaries_temp RENAME TO SDUSsalaries')

# Commit the changes and close the connection
conn.commit()
conn.close()