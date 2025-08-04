from PyQt5.QtCore import QSettings

def get_bearer_token():
    settings = QSettings("Atomwalk", "LogInApp")
    return settings.value("auth_token", "")

# Get db_name from QSettings for dynamic API endpoint
settings = QSettings("Atomwalk", "LogInApp")
user_name = settings.value("user_name", "")
if user_name and "@" in user_name:
    db_name = user_name.split("@")[-1]
else:
    db_name = "LMS_002"  # fallback to default

API_ENDPOINT = f"https://crm.atomwalk.com/lab_api/process_glp_test_data/{db_name}/"

# Other constants
INCOMING_DIR = r"C:/Users/WIN11 24H2/Desktop/Atomwalk/Advia_Interface/SDK/input_files"
PROCESSED_DIR = r"C:/Users/WIN11 24H2/Desktop/Atomwalk/Advia_Interface/SDK/processed_to_ERP"
SERIAL_PORT = "COM4"
BAUDRATE = 9600

TCP_IP = settings.value("tcp_ip", "127.0.0.1")

# Safe conversion with error handling
try:
    tcp_port_value = settings.value("tcp_port", "9200")
    TCP_PORT = int(tcp_port_value) if tcp_port_value else 9200
except (ValueError, TypeError):
    print(f"⚠️ Invalid tcp_port value in QSettings: '{tcp_port_value}'. Using default port 9200.")
    TCP_PORT = 9200