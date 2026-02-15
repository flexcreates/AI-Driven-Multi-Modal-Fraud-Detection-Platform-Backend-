import os
import platform
import subprocess
import sys
import venv
from pathlib import Path

# --- Configuration ---
PROJECT_NAME = "AI-Driven Multi-Modal Fraud Detection Platform (Backend)"
AUTHOR = "Flex"
CONTACT_GITHUB = "https://github.com/flexcreates"
CONTACT_BACKUP = "Abhay"
ERROR_COUNT_FILE = Path("setup_errors.txt")
ERROR_THRESHOLD = 3
VENV_DIR = Path("venv")

# --- Colors ---
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print_header(msg):
        print(f"{Colors.HEADER}{Colors.BOLD}\n=== {msg} ==={Colors.ENDC}")

    @staticmethod
    def print_success(msg):
        print(f"{Colors.OKGREEN}✔ {msg}{Colors.ENDC}")

    @staticmethod
    def print_info(msg):
        print(f"{Colors.OKCYAN}ℹ {msg}{Colors.ENDC}")

    @staticmethod
    def print_warning(msg):
        print(f"{Colors.WARNING}⚠ {msg}{Colors.ENDC}")

    @staticmethod
    def print_error(msg):
        print(f"{Colors.FAIL}✖ {msg}{Colors.ENDC}")

# --- Utilities ---
def get_os_type():
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin": # Mac
        return "unix"
    else: # Linux
        return "unix"

def increment_error_count():
    count = 0
    if ERROR_COUNT_FILE.exists():
        try:
            with open(ERROR_COUNT_FILE, "r") as f:
                content = f.read().strip()
                if content:
                    count = int(content)
        except ValueError:
            pass # Reset if corrupted
    
    count += 1
    with open(ERROR_COUNT_FILE, "w") as f:
        f.write(str(count))
    return count

def check_error_threshold(current_count):
    if current_count >= ERROR_THRESHOLD:
        print(f"\n{Colors.FAIL}{Colors.BOLD}" + "="*60)
        print(f"CRITICAL SETUP FAILURE (Attempt {current_count})")
        print(" It seems you are having trouble setting up the environment.")
        print(f" Please contact {Colors.UNDERLINE}{AUTHOR}{Colors.ENDC}{Colors.FAIL}{Colors.BOLD} immediately at: {CONTACT_GITHUB}")
        print(f" If {AUTHOR} is unavailable, contact {Colors.UNDERLINE}{CONTACT_BACKUP}{Colors.ENDC}{Colors.FAIL}{Colors.BOLD}.")
        print("="*60 + f"{Colors.ENDC}\n")
        return True
    return False

def run_command(command, shell=True, check=True):
    try:
        subprocess.run(command, shell=shell, check=check, text=True, capture_output=False)
    except subprocess.CalledProcessError as e:
        Colors.print_error(f"Command failed: {command}")
        count = increment_error_count()
        check_error_threshold(count)
        sys.exit(1)

# --- Steps ---

def setup_venv():
    Colors.print_header(f"Setting up Virtual Environment ({get_os_type().upper()})")
    
    if VENV_DIR.exists():
        Colors.print_info(f"Virtual environment '{VENV_DIR}' already exists.")
    else:
        Colors.print_info(f"Creating virtual environment at '{VENV_DIR}'...")
        try:
            venv.create(VENV_DIR, with_pip=True)
            Colors.print_success("Virtual environment created.")
        except Exception as e:
            Colors.print_error(f"Failed to create venv: {e}")
            count = increment_error_count()
            check_error_threshold(count)
            sys.exit(1)

def install_dependencies():
    Colors.print_header("Installing Dependencies")
    
    os_type = get_os_type()
    if os_type == "windows":
        pip_path = VENV_DIR / "Scripts" / "pip"
    else:
        pip_path = VENV_DIR / "bin" / "pip"
    
    if not pip_path.exists():
        Colors.print_error(f"Pip not found at expected path: {pip_path}")
        sys.exit(1)

    Colors.print_info("Installing requirements from requirements.txt...")
    run_command(f'"{pip_path}" install --upgrade pip') # Upgrade pip first
    run_command(f'"{pip_path}" install -r requirements.txt')
    Colors.print_success("Dependencies installed successfully.")

def setup_env_file():
    Colors.print_header("Configuring Environment (.env)")
    
    env_path = Path(".env")
    
    # Default values
    default_config = {
        "POSTGRES_USER": "postgres",
        "POSTGRES_PASSWORD": "your_password",
        "POSTGRES_SERVER": "localhost",
        "POSTGRES_PORT": "5432",
        "POSTGRES_DB": "fraud_detection_db",
        "SECRET_KEY": "supersecretkeychangedinproduction",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "30"
    }

    current_config = {}
    
    # Read existing if present to keep current values as defaults
    if env_path.exists():
        Colors.print_info("Existing .env file found. Updating configuration...")
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, val = line.strip().split("=", 1)
                    current_config[key] = val
    else:
        Colors.print_info("No .env file found. Creating new...")

    # Merge checking defaults
    for key, output_val in default_config.items(): # Use defaults for missing keys
         if key not in current_config:
             current_config[key] = output_val

    # Prompt user for database credentials
    print(f"\n{Colors.OKCYAN}Please enter your PostgreSQL credentials (press Enter to keep current/default):{Colors.ENDC}")
    
    db_user = input(f"Database User [{current_config['POSTGRES_USER']}]: ").strip()
    if db_user: current_config['POSTGRES_USER'] = db_user
    
    db_pass = input(f"Database Password [{current_config['POSTGRES_PASSWORD']}]: ").strip()
    if db_pass: current_config['POSTGRES_PASSWORD'] = db_pass
    
    db_name = input(f"Database Name [{current_config['POSTGRES_DB']}]: ").strip()
    if db_name: current_config['POSTGRES_DB'] = db_name

    # Write back to .env
    with open(env_path, "w") as f:
        for key, val in current_config.items():
            f.write(f"{key}={val}\n")
            
    Colors.print_success(".env file configured successfully.")
    return current_config

def init_database():
    Colors.print_header("Initializing Database")
    
    os_type = get_os_type()
    if os_type == "windows":
        python_path = VENV_DIR / "Scripts" / "python"
    else:
        python_path = VENV_DIR / "bin" / "python"
        
    Colors.print_info("Running init_db.py script...")
    run_command(f'"{python_path}" init_db.py')
    Colors.print_success("Database initialized.")

def main():
    Colors.print_header(f"Welcome to {PROJECT_NAME} Setup")
    print(f"OS Detected: {platform.system()} ({platform.release()})")
    print("-" * 50)
    
    try:
        setup_venv()
        install_dependencies()
        setup_env_file()
        init_database()
        
        Colors.print_header("Setup Complete!")
        Colors.print_success("You are ready to go.")
        print(f"\nTo start the server, run:")
        
        if get_os_type() == "windows":
             print(f"  {Colors.BOLD}venv\\Scripts\\activate{Colors.ENDC}")
        else:
             print(f"  {Colors.BOLD}source venv/bin/activate{Colors.ENDC}")
             
        print(f"  {Colors.BOLD}uvicorn SRC.main:app --reload{Colors.ENDC}\n")
        
        # Clear error log on success
        if ERROR_COUNT_FILE.exists():
            os.remove(ERROR_COUNT_FILE)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Setup cancelled by user.{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        Colors.print_error(f"Unexpected error: {e}")
        count = increment_error_count()
        check_error_threshold(count)
        sys.exit(1)

if __name__ == "__main__":
    main()
