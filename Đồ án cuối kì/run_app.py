import os
import sys
import subprocess

# Lấy đường dẫn tuyệt đối đến file app.py
app_path = os.path.join(os.path.dirname(__file__), "querymancer", "app.py")

# Chạy streamlit bằng Python module
subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
