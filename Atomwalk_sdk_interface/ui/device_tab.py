# ui/device_tab.py (Production-Ready Version)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QHBoxLayout, QListWidget, QMessageBox, QComboBox, QStackedWidget, QFormLayout
)
from PyQt5.QtCore import QSettings, Qt, pyqtSignal
import requests
import json

class DeviceTab(QWidget):
    devices_updated = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("Atomwalk", "LogInApp")
        self.logged_devices = []
        self.current_user = self.settings.value("user_name", "").strip()
        self.selected_device_index = -1

        self.setMinimumSize(800, 600)
        self.setStyleSheet("font-size: 15px;")
        self.init_ui()
        self.restore_cached_devices()

    def init_ui(self):
        layout = QVBoxLayout()

        # -------- Authentication Panel --------
        self.device_label = QLabel("Authenticate Your Device:")
        layout.addWidget(self.device_label)

        input_layout = QHBoxLayout()
        self.device_id_input = QLineEdit()
        self.device_id_input.setPlaceholderText("Enter Device ID")

        self.secret_input = QLineEdit()
        self.secret_input.setPlaceholderText("Enter Secret Key")
        self.secret_input.setEchoMode(QLineEdit.Password)

        self.add_device_button = QPushButton("Authenticate Device")
        self.add_device_button.clicked.connect(self.authenticate_device)

        input_layout.addWidget(self.device_id_input)
        input_layout.addWidget(self.secret_input)
        input_layout.addWidget(self.add_device_button)

        layout.addLayout(input_layout)

        # -------- Authenticated Devices List --------
        layout.addWidget(QLabel("Authenticated Devices:"))
        self.device_list_widget = QListWidget()
        self.device_list_widget.itemClicked.connect(self.show_connection_config)
        layout.addWidget(self.device_list_widget)

        self.remove_button = QPushButton("Remove Selected Device")
        self.remove_button.clicked.connect(self.remove_selected_device)
        layout.addWidget(self.remove_button, alignment=Qt.AlignRight)

        # -------- Connection Settings Form --------
        self.connection_label = QLabel("Connection Configuration:")
        self.connection_label.setStyleSheet("font-weight: bold;")
        self.connection_label.hide()
        layout.addWidget(self.connection_label)

        self.connection_type = QComboBox()
        self.connection_type.addItems(["Select", "TCP/IP", "Serial"])
        self.connection_type.currentIndexChanged.connect(self.toggle_connection_inputs)
        self.connection_type.hide()
        layout.addWidget(self.connection_type)

        self.connection_form = QStackedWidget()

        # TCP/IP Fields
        tcp_form = QWidget()
        tcp_layout = QFormLayout()
        self.ip_input = QLineEdit()
        self.port_input = QLineEdit()
        tcp_layout.addRow("IP Address:", self.ip_input)
        tcp_layout.addRow("Port:", self.port_input)
        tcp_form.setLayout(tcp_layout)

        # RS232 Fields
        rs_form = QWidget()
        rs_layout = QFormLayout()
        self.com_input = QLineEdit()
        self.baud_input = QLineEdit()
        rs_layout.addRow("COM Port:", self.com_input)
        rs_layout.addRow("Baudrate:", self.baud_input)
        rs_form.setLayout(rs_layout)

        self.connection_form.addWidget(QWidget())  # Index 0: Placeholder
        self.connection_form.addWidget(tcp_form)  # Index 1: TCP/IP
        self.connection_form.addWidget(rs_form)   # Index 2: RS232
        self.connection_form.hide()

        layout.addWidget(self.connection_form)

        self.save_config_btn = QPushButton("Save Configuration")
        self.save_config_btn.clicked.connect(self.save_connection_config)
        self.save_config_btn.hide()
        layout.addWidget(self.save_config_btn, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def authenticate_device(self):
        device_id = self.device_id_input.text().strip()
        secret = self.secret_input.text().strip()

        if not device_id or not secret:
            QMessageBox.warning(self, "Missing Info", "Please enter Device ID and Secret Key.")
            return

        db_name = self.settings.value("user_name", "").split("@")[-1]
        if not db_name:
            QMessageBox.critical(self, "Error", "User DB not found. Please log in again.")
            return
            
        url = f"https://crm.atomwalk.com/hr_api/get_device_token/{db_name}/"
        try:
            response = requests.post(url, json={"device_id": device_id, "secret_key": secret})
            if response.status_code == 200:
                token = response.json().get("token", "")
                for dev in self.logged_devices:
                    if dev["device_id"] == device_id and dev.get("user") == self.current_user:
                        QMessageBox.information(self, "Already Authenticated", "This device is already authenticated.")
                        return

                entry = f"{device_id}@{db_name} - Authenticated"
                self.logged_devices.append({
                    "device_id": device_id,
                    "secret": secret,
                    "db": db_name,
                    "token": token,
                    "user": self.current_user
                })
                self.device_list_widget.addItem(entry)
                self.save_devices()
                self.devices_updated.emit(self.logged_devices)
                self.device_id_input.clear()
                self.secret_input.clear()
            else:
                error = response.json().get("error", "Invalid credentials or device not found.")
                QMessageBox.warning(self, "Auth Failed", f"Server response: {error}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"API call failed:\n{e}")

    def show_connection_config(self):
        self.selected_device_index = self.device_list_widget.currentRow()
        self.connection_label.show()
        self.connection_type.show()
        self.connection_form.show()
        self.save_config_btn.show()

    def toggle_connection_inputs(self, index):
        self.connection_form.setCurrentIndex(index)

    def save_connection_config(self):
        if self.selected_device_index < 0:
            QMessageBox.warning(self, "No Device Selected", "Please select a device to configure.")
            return

        selected = self.logged_devices[self.selected_device_index]
        conn_type = self.connection_type.currentText()

        if conn_type == "TCP/IP":
            ip = self.ip_input.text().strip()
            port = self.port_input.text().strip()
            selected["connection"] = {
                "type": "TCP/IP",
                "ip": ip,
                "port": port
            }
            # Save to QSettings for SDK config.py
            self.settings.setValue("tcp_ip", ip)
            self.settings.setValue("tcp_port", port)
            # Update advia_proxy/config.json
            try:
                config_path = "C:/Users/WIN11 24H2/Desktop/Atomwalk/Advia_Interface/advia_proxy/config.json"
                with open(config_path, "r") as f:
                    config = json.load(f)
                config["tcp_ip"] = ip
                config["tcp_port"] = int(port)
                config["connection_mode"] = "tcp"
                with open(config_path, "w") as f:
                    json.dump(config, f, indent=2)
            except Exception as e:
                QMessageBox.warning(self, "Config Error", f"Failed to update proxy config: {e}")
        elif conn_type == "RS232":
            selected["connection"] = {
                "type": "RS232",
                "com_port": self.com_input.text().strip(),
                "baudrate": self.baud_input.text().strip()
            }
        else:
            QMessageBox.warning(self, "Select Type", "Please choose a connection type.")
            return

        self.logged_devices[self.selected_device_index] = selected
        self.save_devices()
        QMessageBox.information(self, "Saved", "Connection configuration saved.")

    def remove_selected_device(self):
        row = self.device_list_widget.currentRow()
        if row < 0:
            QMessageBox.information(self, "No Selection", "Select a device to remove.")
            return

        confirm = QMessageBox.question(self, "Confirm Removal", "Are you sure you want to remove this device?")
        if confirm != QMessageBox.Yes:
            return

        del self.logged_devices[row]
        self.device_list_widget.takeItem(row)
        self.save_devices()
        self.devices_updated.emit(self.logged_devices)

    def restore_cached_devices(self):
        saved_devices = self.settings.value("logged_devices", [])
        if saved_devices:
            for d in saved_devices:
                if isinstance(d, dict) and "device_id" in d and d.get("user") == self.current_user:
                    entry = f"{d['device_id']}@{d.get('db', 'unknown')} - Authenticated"
                    self.logged_devices.append(d)
                    self.device_list_widget.addItem(entry)
            self.devices_updated.emit(self.logged_devices)

    def save_devices(self):
        self.settings.setValue("logged_devices", self.logged_devices)

    def get_logged_devices(self):
        return self.logged_devices
