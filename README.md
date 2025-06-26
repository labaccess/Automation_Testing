# 📘 Robot Framework ADSL CPE Automation with Database and Flask UI

This repository provides a complete setup for testing ADSL CPE devices (Huawei, ZTE, Nokia) using Robot Framework. It automates test execution, stores results in an SQLite database, and provides a Flask-based web interface to view and manage results.

---

## 📂 Project Structure

```
Automation_Testing/
├── Resources/
│   └── db_listener.py              # Robot Framework listener to log results to SQLite
├── runner_files/
│   └── Demo.robot                  # Example test suite
├── Results/                        # Auto-created folders for each run
│   └── Run_<timestamp>/           # Log, report, output.xml per run
├── templates/
│   ├── index.html                 # Flask: All test runs view
│   └── run_details.html           # Flask: Run-specific test case results
├── app.py                          # Flask web app
├── runner.py                       # Custom script to execute test with dynamic results folder
├── test_results.db                 # SQLite database
├── README.md                       # This file
└── requirements.txt                # Required Python libraries
```

---

## 🧪 Robot Framework Test Execution

### ▶️ Run tests with automatic results folder and DB logging:

```bash
python runner.py
```

This script will:

* Generate a results folder: `Results/Run_<timestamp>`
* Run tests using Robot Framework
* Store test results and file paths in SQLite database

---

## 📦 SQLite Database Schema

```sql
CREATE TABLE IF NOT EXISTS test_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

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
);

CREATE TABLE IF NOT EXISTS run_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER,
    filename TEXT,
    filepath TEXT,
    FOREIGN KEY(run_id) REFERENCES test_runs(id)
);
```

---

## 🌐 Flask Web App

### ▶️ Launch Flask UI

```bash
python app.py
```

### 🔗 Features

* List all test runs
* View details of each run (test case name, status, message)
* Link to download/view `report.html`, `log.html` per run

### 📁 Serve Report Files

To serve reports using Flask:

```python
from flask import send_from_directory

@app.route('/report/<path:subpath>')
def serve_result_file(subpath):
    return send_from_directory("Results", subpath)
```

Then in HTML:

```html
<a href="{{ url_for('serve_result_file', subpath=r['report_path']) }}" target="_blank">View Report</a>
```

---

## 📸 Scroll & Capture Entire Page (Robot Framework)

### Scroll Element to Top

```robot
Execute JavaScript    arguments[0].scrollIntoView(true);    xpath=//h3[text()='WiFi Settings']
```

### Full Page Screenshot (Headless Chrome)

```robot
${chrome options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
Call Method    ${chrome options}    add_argument    --headless
Call Method    ${chrome options}    add_argument    --window-size=1920,3000
Create WebDriver    Chrome    chrome_options=${chrome options}
Capture Page Screenshot    full_page.png
```

---

## 🔄 Requirements

```text
robotframework
robotframework-seleniumlibrary
flask
selenium
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## 🛠 Common Issues

### ❌ `database is locked`

Make sure only one connection is open at a time. Use proper `conn.close()` in all scripts.

### ❌ `ModuleNotFoundError: No module named 'db_listener'`

Ensure the script is run from the correct directory or use `PYTHONPATH` properly.

### ❌ `ElementNotInteractableException`

Use waits and `Scroll Element Into View` before clicking:

```robot
Wait Until Element Is Visible    xpath=//button
Scroll Element Into View         xpath=//button
Click Element
```
