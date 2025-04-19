import subprocess
import threading
import time
import os

def run_fastapi():
    subprocess.call(["uvicorn", "fastapi_app:app", "--reload"])

def run_streamlit():
    # Optional: wait to make sure FastAPI is up
    time.sleep(2)
    os.system("streamlit run streamlit_app.py")

# Start FastAPI in a new thread
fastapi_thread = threading.Thread(target=run_fastapi)
fastapi_thread.start()

# Run Streamlit in main thread (or another thread if you prefer)
run_streamlit()
