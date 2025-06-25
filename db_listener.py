from robot.api import logger
import sqlite3
from robot import result, running
from robot.api.interfaces import ListenerV3


class DBListener(ListenerV3):
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, db_path="test_results.db"):
        self.ROBOT_LIBRARY_LISTENER = self
        logger.console("🚀 DBListener initialized")
        self.conn = sqlite3.connect(db_path, timeout=5)
        self.cursor = self.conn.cursor()
        self._create_tables()
        self.run_id = self._create_test_run()
        logger.console(f"📌 New test run ID = {self.run_id}")

    def _create_tables(self):
        logger.console(f"📌 Create test_runs table ")
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT (datetime('now'))
            )
        ''')
        logger.console(f"📌 Create test_results table ")
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER,
                suite_name TEXT,
                test_name TEXT,
                status TEXT,
                start_time TEXT,
                end_time TEXT,
                message TEXT
            )
        ''')
        logger.console(f"📌 Create run_files table ")
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS run_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER,
            filename TEXT,
            filepath TEXT,
            FOREIGN KEY(run_id) REFERENCES test_runs(id)
        )
        ''')
        self.conn.commit()

    def _create_test_run(self):
        self.cursor.execute("INSERT INTO test_runs DEFAULT VALUES")
        self.conn.commit()
        return self.cursor.lastrowid

    def end_test(self, data, result):
        logger.console(f"📍 end_test() called for: {result.name}")
        try:
            suite_name = result.parent.name
            test_name = result.name
            status = result.status
            start_time = result.start_time or ""
            end_time = result.end_time or ""
            message = result.message or ""

            self.cursor.execute('''
                INSERT INTO test_results (run_id, suite_name, test_name, status, start_time, end_time, message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (self.run_id, suite_name, test_name, status, start_time, end_time, message))
            self.conn.commit()

            logger.console(f"✅ Inserted result: {test_name} ({status})")

        except Exception as e:
            logger.console(f"❌ Failed to insert result: {e}")

    def close(self):
        try:
            self.conn.close()
            logger.console("🧹 Database connection closed.")
        except Exception as e:
            logger.console(f"❌ DB close failed: {e}")
    
def get_latest_run_id():
    db = sqlite3.connect("test_results.db", timeout=5)
    cursor = db.cursor()
    cursor.execute("SELECT MAX(id) FROM test_runs")
    result = cursor.fetchone()
    db.close()
    return result[0] if result else None


