# app.py
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3

app = Flask(__name__)

DB_PATH = 'test_results.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    runs = conn.execute('SELECT * FROM test_runs ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', runs=runs)

@app.route('/run/<int:run_id>')
def run_details(run_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get test results
    cursor.execute("SELECT test_name, status, start_time, end_time, message FROM test_results WHERE run_id = ?", (run_id,))
    results = cursor.fetchall()
    print(f"Results : {results}")

    # Get report file path (only one per run expected)
    cursor.execute("SELECT filepath FROM run_files WHERE run_id = ? AND filename = 'report.html'", (run_id,))
    report_row = cursor.fetchone()
    report_path = report_row[0] if report_row else None
    print(f"Report_path : {report_path}")

    conn.close()
    return render_template("run_details.html", run_id=run_id, results=results, report_path=report_path)

# @app.route('/results/<path:filename>')
# def serve_results(filename):
#     return send_from_directory('Results', filename)

@app.route('/results/<path:subpath>')
def serve_result_file(subpath):
    return send_from_directory('static/Results', subpath)


if __name__ == '__main__':
    app.run(debug=True)
