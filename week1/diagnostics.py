import os
import sys
print(f"Python version: {sys.version}")
import platform
import subprocess
import shutil
import time
import ssl
import tempfile
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Fix lỗi ký tự unicode trên Windows console, chỉ thực hiện nếu có buffer
if sys.platform == "win32":
    try:
        import io
        if hasattr(sys.stdout, "buffer"):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    except Exception as e:
        pass  # Ignore if running in an environment that doesn't support this



class Diagnostics:
    FILENAME = 'report.txt'

    def __init__(self):
        self.errors = []
        self.warnings = []
        if os.path.exists(self.FILENAME):
            os.remove(self.FILENAME)

    def log(self, message):
        print(message)
        with open(self.FILENAME, 'a', encoding='utf-8') as f:
            f.write(message + "\n")

    def start(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log(f"Starting diagnostics at {now}\n")

    def end(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log(f"\n\nCompleted diagnostics at {now}\n")
        print("\nPlease send these diagnostics to me at ed@edwarddonner.com")
        print(f"Either copy & paste the above output into an email, or attach the file {self.FILENAME} that has been created in this directory.")

    def _log_error(self, message):
        self.log(f"ERROR: {message}")
        self.errors.append(message)

    def _log_warning(self, message):
        self.log(f"WARNING: {message}")
        self.warnings.append(message)

    def run(self):
        self.start()
        self._step1_system_info()
        self._step2_check_files()
        self._step3_git_repo()
        self._step4_check_env_file()
        self._step5_anaconda_check()
        self._step6_virtualenv_check()
        self._step7_network_connectivity()
        self._step8_environment_variables()
        self._step9_additional_diagnostics()

        if self.warnings:
            self.log("\n===== Warnings Found =====")
            self.log("The following warnings were detected. They might not prevent the program from running but could cause unexpected behavior:")
            for warning in self.warnings:
                self.log(f"- {warning}")

        if self.errors:
            self.log("\n===== Errors Found =====")
            self.log("The following critical issues were detected. Please address them before proceeding:")
            for error in self.errors:
                self.log(f"- {error}")

        if not self.errors and not self.warnings:
            self.log("\n✅ All diagnostics passed successfully!")

        self.end()

    def _step1_system_info(self):
        self.log("===== System Information =====")
        try:
            system = platform.system()
            self.log(f"Operating System: {system}")

            if system == "Windows":
                release, version, *_ = platform.win32_ver()
                self.log(f"Windows Release: {release}")
                self.log(f"Windows Version: {version}")
            elif system == "Darwin":
                release, *_ = platform.mac_ver()
                self.log(f"MacOS Version: {release}")
            else:
                self.log(f"Platform: {platform.platform()}")

            self.log(f"Architecture: {platform.architecture()}")
            self.log(f"Machine: {platform.machine()}")
            self.log(f"Processor: {platform.processor()}")

            try:
                import psutil
                ram = psutil.virtual_memory()
                total_ram_gb = ram.total / (1024 ** 3)
                available_ram_gb = ram.available / (1024 ** 3)
                self.log(f"Total RAM: {total_ram_gb:.2f} GB")
                self.log(f"Available RAM: {available_ram_gb:.2f} GB")
                if available_ram_gb < 2:
                    self._log_warning(f"Low available RAM: {available_ram_gb:.2f} GB")
            except ImportError:
                self._log_warning("psutil module not found. Cannot determine RAM information.")

            total, used, free = shutil.disk_usage(os.path.expanduser("~"))
            free_gb = free / (1024 ** 3)
            self.log(f"Free Disk Space: {free_gb:.2f} GB")
            if free_gb < 5:
                self._log_warning(f"Low disk space: {free_gb:.2f} GB free")
        except Exception as e:
            self._log_error(f"System information check failed: {e}")

    def _step2_check_files(self):
        self.log("\n===== File System Information =====")
        try:
            cwd = os.getcwd()
            self.log(f"Current Directory: {cwd}")
            self.log(f"Write permission: {'OK' if os.access(cwd, os.W_OK) else 'No write permission'}")

            files = os.listdir(cwd)
            if files:
                self.log("\nFiles in Current Directory:")
                for f in sorted(files):
                    self.log(f" - {f}")
            else:
                self.log("No files found in the current directory.")

        except Exception as e:
            self._log_error(f"File system check failed: {e}")

    def _step3_git_repo(self):
        self.log("\n===== Git Repository Information =====")
        try:
            result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                self.log("This is a git repository.")
            else:
                self._log_warning("Not a git repository")
        except FileNotFoundError:
            self._log_warning("Git is not installed or not in PATH")
        except Exception as e:
            self._log_error(f"Git repository check failed: {e}")

    def _step4_check_env_file(self):
        self.log("\n===== Environment File Check =====")
        try:
            result = subprocess.run(['git', 'rev-parse', '--show-toplevel'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                git_root = result.stdout.strip()
                env_path = os.path.join(git_root, '.env')

                if os.path.isfile(env_path):
                    self.log(f".env file exists at: {env_path}")
                    try:
                        with open(env_path, 'r') as f:
                            has_api_key = any(line.strip().startswith('GEMINI_API_KEY=') for line in f)
                        if has_api_key:
                            self.log("GEMINI_API_KEY found in .env file")
                        else:
                            self._log_warning("GEMINI_API_KEY not found in .env file")
                    except Exception as e:
                        self._log_error(f"Cannot read .env file: {e}")
                else:
                    self._log_warning(".env file not found in project root")

                # Check for additional .env files
                for root, _, files in os.walk(git_root):
                    full_path = os.path.join(root, '.env')
                    if '.env' in files and full_path != env_path:
                        self._log_warning(f"Additional .env file found at: {full_path}")
            else:
                self._log_warning("Git root directory not found. Cannot perform .env file check.")
        except Exception as e:
            self._log_error(f"Environment file check failed: {e}")

    def _step5_anaconda_check(self):
        self.log("\n===== Anaconda Environment Check =====")
        conda_env = os.environ.get('CONDA_DEFAULT_ENV')
        if conda_env:
            self.log(f"Active Anaconda environment: {conda_env}")
        else:
            self._log_warning("No active Anaconda environment detected")

    def _step6_virtualenv_check(self):
        self.log("\n===== Virtualenv Check =====")
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            self.log("Virtual environment is active.")
        else:
            self._log_warning("Neither virtualenv nor Anaconda environment is active")

    def _step7_network_connectivity(self):
        self.log("\n===== Network Connectivity Check =====")
        try:
            ssl_version = ssl.OPENSSL_VERSION
            self.log(f"SSL Version: {ssl_version}")
            import socket
            socket.create_connection(("www.google.com", 443), timeout=5)
            self.log("Internet connection: OK")
        except Exception as e:
            self._log_error(f"Network connectivity check failed: {e}")

    def _step8_environment_variables(self):
        self.log("\n===== Environment Variables Check =====")
        try:
            pythonpath = os.environ.get('PYTHONPATH')
            if pythonpath:
                self.log("\nPYTHONPATH:")
                for path in pythonpath.split(os.pathsep):
                    self.log(f" - {path}")
            else:
                self.log("\nPYTHONPATH is not set.")

            self.log("\nPython sys.path:")
            for path in sys.path:
                self.log(f" - {path}")

            load_dotenv()
            api_key = os.environ.get('GEMINI_API_KEY')
            if api_key:
                self.log("GEMINI_API_KEY is set after calling load_dotenv()")
                if not api_key.startswith('sk-') or len(api_key) < 10:
                    self._log_warning("GEMINI_API_KEY format looks incorrect")
            else:
                self._log_warning("GEMINI_API_KEY environment variable is not set after calling load_dotenv()")
        except Exception as e:
            self._log_error(f"Environment variables check failed: {e}")

    def _step9_additional_diagnostics(self):
        self.log("\n===== Additional Diagnostics =====")
        try:
            cwd = Path.cwd().resolve()
            home = Path.home().resolve()
            if cwd.drive != home.drive:
                self._log_warning(f"Project directory ({cwd}) and user home directory ({home}) are on different drives ({cwd.drive} vs. {home.drive}). This might affect performance in some cases.")
            else:
                self.log("Project and user home are on the same drive.")
        except Exception as e:
            self._log_error(f"Additional diagnostics failed: {e}")

if __name__ == "__main__":
    diagnostics = Diagnostics()
    diagnostics.run()