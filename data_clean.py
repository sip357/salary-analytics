import sqlite3

VALID_CURRENCIES = {'USD', 'EUR', 'GBP', 'CAD', 'AUD'}
VALID_PERIODS = {'hourly', 'daily', 'weekly', 'monthly', 'annual', 'yearly'}


def is_number(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def validate_row(row):
    id_, location, job_title, min_salary, max_salary, median_salary, salary_period, salary_currency = row

    if id_ is None:
        return False

    if not isinstance(location, str) or not location.strip(): # Check if location is a non-empty string
        return False

    if not isinstance(job_title, str) or not job_title.strip(): # Check if job_title is a non-empty string
        return False

    if not (is_number(min_salary) and is_number(max_salary) and is_number(median_salary)): # Check if salaries are numbers
        return False

    min_salary = float(min_salary)
    max_salary = float(max_salary)
    median_salary = float(median_salary)

    if min_salary < 0 or max_salary < 0 or median_salary < 0: # Check if salaries are non-negative
        return False

    if min_salary > max_salary: # Check if min_salary is not greater than max_salary
        return False

    if not (min_salary <= median_salary <= max_salary): # Check if median_salary is between min_salary and max_salary
        return False

    if salary_currency is not None:
        if not isinstance(salary_currency, str) or salary_currency.upper() not in VALID_CURRENCIES:
            return False

    if salary_period is not None:
        if not isinstance(salary_period, str) or salary_period.lower() not in VALID_PERIODS:
            return False

    return True


def clean_salaries(database_path='sd_salaries_us.db'):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('SELECT id, location, job_title, min_salary, max_salary, median_salary, salary_period, salary_currency FROM SDUSsalaries')
    rows = cursor.fetchall()

    cursor.execute('DROP TABLE IF EXISTS SDUSsalaries_temp')
    cursor.execute('''
    CREATE TABLE SDUSsalaries_temp (
        id INTEGER,
        location TEXT,
        job_title TEXT,
        min_salary REAL,
        max_salary REAL,
        median_salary REAL,
        salary_period TEXT,
        salary_currency TEXT
    )
    ''')

    inserted = 0
    for row in rows:
        if validate_row(row):
            cursor.execute(
                'INSERT OR IGNORE INTO SDUSsalaries_temp (id, location, job_title, min_salary, max_salary, median_salary, salary_period, salary_currency) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                row,
            )
            inserted += 1

    cursor.execute('DROP TABLE SDUSsalaries')
    cursor.execute('ALTER TABLE SDUSsalaries_temp RENAME TO SDUSsalaries')
    conn.commit()
    conn.close()

    return inserted, len(rows)


if __name__ == '__main__':
    kept, total = clean_salaries()
    print(f'Validated rows: {kept} / {total}')
