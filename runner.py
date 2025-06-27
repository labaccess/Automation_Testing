import os
import datetime
import subprocess
import sqlite3
import argparse
from db_listener import get_latest_run_id  # You’ll write this too
import shutil


def save_run_files_to_db(run_id, output_dir):
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

# Path to your virtual environment Python
python_path = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")

# Generate timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Create result folder
output_dir = os.path.join("Results", f"Run_{timestamp}")
os.makedirs(output_dir, exist_ok=True)


parser = argparse.ArgumentParser(description="Run Robot Framework test with model resource.")
parser.add_argument('--model', type=str, required=True, help="Path to the Robot model resource file")

args = parser.parse_args()
model_robot_file = args.model

model_resource_path = f"../CPE_Data/{model_robot_file}.robot"
file_path = f'CPE_Data/{model_robot_file}.robot'
if os.path.exists(file_path):
    print("✅ File exists.")
    cmd = [
    python_path, "-m", "robot",
    "-d", output_dir,
    "--listener", f"db_listener.DBListener",
    f"--variable", f"MODEL_RESOURCE:{model_resource_path}",  # 👈 inject as variable
    "runner_files\\CPE_TC.robot"]
    print(cmd)
    subprocess.run(cmd)

    # After Robot run completes
    run_id = get_latest_run_id()
    save_run_files_to_db(run_id, output_dir)
    static_results_dir = os.path.join("Flask_Data\\static", output_dir)  # 'static/Results/Run_...'
    os.makedirs(os.path.dirname(static_results_dir), exist_ok=True)
    shutil.copytree(output_dir, static_results_dir, dirs_exist_ok=True)
    
else:
    print("❌ File does not exist.")








