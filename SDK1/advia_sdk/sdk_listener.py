import os
import datetime
import serial
import socket
from pathlib import Path
import uuid
import hashlib

from advia_sdk.config import INPUT_DIR, LOG_FILE, SERIAL_PORT, BAUDRATE, TCP_IP, TCP_PORT

# Ensure the input directory exists
Path(INPUT_DIR).mkdir(parents=True, exist_ok=True)

def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {msg}\n")

def generate_filename(data):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    unique = uuid.uuid4().hex[:8]
    checksum = hashlib.sha256(data.encode()).hexdigest()[:8]
    return f"advia_{timestamp}_{unique}_{checksum}.astm"

def save_to_input(data):
    filename = generate_filename(data)
    file_path = os.path.join(INPUT_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)
    log(f"✅ Saved input file: {filename}")

def listen_serial():
    log("🔌 SDK Serial Listener: Listening...")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=5)
        buffer = ""
        while True:
            chunk = ser.read().decode(errors="ignore")
            buffer += chunk
            if "\x04" in chunk:  # ASTM EOT
                save_to_input(buffer)
                buffer = ""
    except Exception as e:
        log(f"❌ Serial Read Error: {e}")

def listen_tcp():
    log(f"🌐 SDK TCP Listener on {TCP_IP}:{TCP_PORT}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        conn, addr = s.accept()
        log(f"🔗 Connected to {addr}")
        buffer = ""
        while True:
            data = conn.recv(1024).decode(errors="ignore")
            if not data:
                break
            buffer += data
            if "\x04" in data:
                save_to_input(buffer)
                buffer = ""
    except Exception as e:
        log(f"❌ TCP Read Error: {e}")

if __name__ == "__main__":
    log("🚀 SDK Listener started")

    # 🟢 Choose the mode you want to run
    # listen_serial()
    # OR
    # listen_tcp()
