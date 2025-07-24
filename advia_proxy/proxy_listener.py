import os
import json
import datetime
import serial
import socket
from pathlib import Path
import uuid
import hashlib

# Load config
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "config.json")

with open(config_path) as f:
    config = json.load(f)

backup_dir = Path(config["backup_dir"])
log_dir = Path(config["log_dir"])
backup_dir.mkdir(parents=True, exist_ok=True)
log_dir.mkdir(parents=True, exist_ok=True)

def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_dir / "listener.log", "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {msg}\n")

# ✅ Secure and unique filename generator
def generate_secure_filename(data):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # milliseconds
    short_uuid = uuid.uuid4().hex[:8]
    hash_part = hashlib.sha256(data.encode()).hexdigest()[:8]  # Optional: integrity check
    return f"advia_{ts}_{short_uuid}_{hash_part}.astm"

def save_astm_message(data):
    filename = generate_secure_filename(data)
    filepath = backup_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data)
    log(f"✅ Saved ASTM file: {filename}")

def read_from_serial():
    log("🔌 Serial Mode: Listening...")
    try:
        ser = serial.Serial(config["serial_port"], config["baudrate"], timeout=5)
        buffer = ""
        while True:
            chunk = ser.read().decode(errors="ignore")
            buffer += chunk
            if "\x04" in chunk:  # ASTM EOT (End of Transmission)
                save_astm_message(buffer)
                buffer = ""
    except Exception as e:
        log(f"❌ Serial Read Error: {e}")

def read_from_tcp():
    log(f"🌐 TCP Mode: Listening on {config['tcp_ip']}:{config['tcp_port']}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((config["tcp_ip"], config["tcp_port"]))
        s.listen(1)
        conn, addr = s.accept()
        log(f"🔗 Connected to {addr}")
        buffer = ""
        while True:
            data = conn.recv(1024).decode(errors="ignore")
            if not data:
                break
            buffer += data
            if "\x04" in data:  # ASTM EOT
                save_astm_message(buffer)
                buffer = ""
    except Exception as e:
        log(f"❌ TCP Read Error: {e}")
def activate_proxy():
    log("🛡️ Proxy Listener manually activated from interface.")
    log("⚠️ SDK unavailable. Awaiting manual or backup data...")
print("🕐 Proxy Listener is idle, waiting for manual file drop.")
if __name__ == "__main__":
   activate_proxy()
