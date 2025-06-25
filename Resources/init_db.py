import sqlite3

conn = sqlite3.connect('test_results.db')  # Creates test_results.db
cursor = conn.cursor()

# Create run metadata table
cursor.execute('''
CREATE TABLE IF NOT EXISTS test_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT
)
''')

# Create test results table
cursor.execute('''
CREATE TABLE IF NOT EXISTS test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER,
    suite_name TEXT,
    test_name TEXT,
    status TEXT,
    start_time TEXT,
    end_time TEXT,
    message TEXT,
    FOREIGN KEY(run_id) REFERENCES test_runs(id)
)
''')

conn.commit()
conn.close()
print("✅ SQLite database initialized: test_results.db")
