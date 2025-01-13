from flask import Flask, render_template
import sqlite3
import pandas as pd
import plotly.express as px
import plotly as plt
import json

app = Flask(__name__)

@app.route("/")
def dashboard():
    # Connect to SQLite
    conn = sqlite3.connect("sd_salaries_us.db")
    query = "SELECT * FROM SDUSsalaries"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Create a bar chart for average salary by job title
    fig = px.bar(df, x="location", y="median_salary", color="min_salary", title="Average Salary of a Software Dev by US city")
    graphJSON = json.dumps(fig, cls=plt.utils.PlotlyJSONEncoder)

    return render_template("dashboard.html", graphJSON=graphJSON)

if __name__ == "__main__":
    app.run(debug=True)
