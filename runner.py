import os
import datetime
import subprocess
import sqlite3


# Path to your virtual environment Python
python_path = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")

# Generate timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Create result folder
output_dir = os.path.join("Results", f"Run_{timestamp}")
os.makedirs(output_dir, exist_ok=True)


# Robot command using venv python
cmd = [
    python_path, "-m", "robot",
    "-d", output_dir,
    "--listener", f"db_listener.DBListener",
    "runner_files\\CPE_Testing.robot"
]

print(cmd)
subprocess.run(cmd)


def save_run_files_to_db(run_id, output_dir):
    import sqlite3

    if not run_id:
        print("❌ ERROR: run_id is None. Cannot insert files.")
        return

    db = sqlite3.connect("test_results.db")
    cursor = db.cursor()

    try:
        for file in os.listdir(output_dir):
            full_path = os.path.join(output_dir, file).replace("\\", "/")
            if os.path.isfile(full_path):
                print(f"📁 Storing: {file} → {full_path}")
                cursor.execute(
                    "INSERT INTO run_files (run_id, filename, filepath) VALUES (?, ?, ?)",
                    (run_id, file, os.path.join(f"Run_{timestamp}", file).replace("\\", "/"))
                )

        db.commit()
        print("✅ Run files stored in DB")

    except Exception as e:
        print(f"❌ Error storing run files: {e}")

    finally:
        db.close()

# After Robot run completes
from db_listener import get_latest_run_id  # You’ll write this too
run_id = get_latest_run_id()
save_run_files_to_db(run_id, output_dir)



import shutil

static_results_dir = os.path.join("Flask_Data\\static", output_dir)  # 'static/Results/Run_...'
os.makedirs(os.path.dirname(static_results_dir), exist_ok=True)
shutil.copytree(output_dir, static_results_dir, dirs_exist_ok=True)
