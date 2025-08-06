# ui/iot_device_tab.py - IOT Device Authentication Tab

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QHBoxLayout, QListWidget, QMessageBox, QComboBox, QFormLayout,
    QGroupBox
)
from PyQt5.QtCore import QSettings, Qt, pyqtSignal, QTimer
import requests
import json
import subprocess
import sys
import os

class IOTDeviceTab(QWidget):
    devices_updated = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("Atomwalk", "LogInApp")
        self.authenticated_devices = []
        self.current_user = self.settings.value("user_name", "").strip()
        self.selected_device_index = -1
        self.scan_timer = QTimer()
        self.scan_timer.timeout.connect(self.scan_iot_devices)

        self.setMinimumSize(800, 600)
        self.setStyleSheet("font-size: 15px;")
        self.init_ui()
        self.restore_cached_devices()

    def init_ui(self):
        layout = QVBoxLayout()

        # -------- Device Discovery Panel --------
        discovery_group = QGroupBox("IOT Device Discovery")
        discovery_layout = QVBoxLayout()
        
        # Auto-scan section
        scan_layout = QHBoxLayout()
        self.scan_button = QPushButton("🔍 Scan for IOT Devices")
        self.scan_button.clicked.connect(self.start_device_scan)
        self.scan_status = QLabel("Ready to scan")
        self.scan_status.setStyleSheet("color: #666; font-style: italic;")
        
        scan_layout.addWidget(self.scan_button)
        scan_layout.addWidget(self.scan_status)
        scan_layout.addStretch()
        
        discovery_layout.addLayout(scan_layout)
        
        # Manual device entry
        manual_layout = QHBoxLayout()
        self.device_id_input = QLineEdit()
        self.device_id_input.setPlaceholderText("Enter IOT Device ID (e.g., SENSOR_001)")
        
        self.device_type_combo = QComboBox()
        self.device_type_combo.addItems(["Temperature Sensor", "Humidity Sensor", "Pressure Sensor", "Motion Sensor", "Custom"])
        
        self.add_manual_button = QPushButton("Add Device Manually")
        self.add_manual_button.clicked.connect(self.add_device_manually)
        
        manual_layout.addWidget(QLabel("Device ID:"))
        manual_layout.addWidget(self.device_id_input)
        manual_layout.addWidget(QLabel("Type:"))
        manual_layout.addWidget(self.device_type_combo)
        manual_layout.addWidget(self.add_manual_button)
        
        discovery_layout.addLayout(manual_layout)
        discovery_group.setLayout(discovery_layout)
        layout.addWidget(discovery_group)

        # -------- Device Authentication Panel --------
        auth_group = QGroupBox("Device Authentication")
        auth_layout = QVBoxLayout()
        
        auth_input_layout = QHBoxLayout()
        self.auth_key_input = QLineEdit()
        self.auth_key_input.setPlaceholderText("Enter Authentication Key")
        self.auth_key_input.setEchoMode(QLineEdit.Password)
        
        self.authenticate_button = QPushButton("🔐 Authenticate Device")
        self.authenticate_button.clicked.connect(self.authenticate_device)
        
        auth_input_layout.addWidget(QLabel("Auth Key:"))
        auth_input_layout.addWidget(self.auth_key_input)
        auth_input_layout.addWidget(self.authenticate_button)
        
        auth_layout.addLayout(auth_input_layout)
        auth_group.setLayout(auth_layout)
        layout.addWidget(auth_group)

        # -------- Authenticated Devices List --------
        devices_group = QGroupBox("Authenticated IOT Devices")
        devices_layout = QVBoxLayout()
        
        self.device_list_widget = QListWidget()
        self.device_list_widget.itemClicked.connect(self.select_device)
        devices_layout.addWidget(self.device_list_widget)
        
        device_buttons_layout = QHBoxLayout()
        self.remove_button = QPushButton("🗑️ Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected_device)
        
        self.test_connection_button = QPushButton("🔗 Test Connection")
        self.test_connection_button.clicked.connect(self.test_device_connection)
        
        device_buttons_layout.addWidget(self.remove_button)
        device_buttons_layout.addWidget(self.test_connection_button)
        device_buttons_layout.addStretch()
        
        devices_layout.addLayout(device_buttons_layout)
        devices_group.setLayout(devices_layout)
        layout.addWidget(devices_group)

        self.setLayout(layout)

    def start_device_scan(self):
        """Start scanning for IOT devices"""
        self.scan_status.setText("Scanning for devices...")
        self.scan_button.setEnabled(False)
        
        # Simulate device discovery (replace with actual IOT device discovery)
        self.scan_timer.start(2000)  # Scan for 2 seconds

    def scan_iot_devices(self):
        """Simulate IOT device discovery"""
        self.scan_timer.stop()
        self.scan_button.setEnabled(True)
        
        # Simulate found devices (replace with actual discovery)
        discovered_devices = [
            {"id": "TEMP_SENSOR_001", "type": "Temperature Sensor", "status": "Available"},
            {"id": "HUMIDITY_SENSOR_002", "type": "Humidity Sensor", "status": "Available"},
            {"id": "MOTION_SENSOR_003", "type": "Motion Sensor", "status": "Available"}
        ]
        
        self.scan_status.setText(f"Found {len(discovered_devices)} devices")
        
        # Show discovered devices in a message box
        if discovered_devices:
            device_list = "\n".join([f"• {d['id']} ({d['type']})" for d in discovered_devices])
            QMessageBox.information(self, "Discovered Devices", 
                                  f"Found the following IOT devices:\n\n{device_list}\n\n"
                                  "You can add them manually using their Device ID.")

    def add_device_manually(self):
        """Add a device manually"""
        device_id = self.device_id_input.text().strip()
        device_type = self.device_type_combo.currentText()
        
        if not device_id:
            QMessageBox.warning(self, "Input Error", "Please enter a Device ID")
            return
        
        # Check if device already exists
        if any(d['id'] == device_id for d in self.authenticated_devices):
            QMessageBox.warning(self, "Device Exists", "This device is already in the list")
            return
        
        # Add to list (not authenticated yet)
        device_info = {
            'id': device_id,
            'type': device_type,
            'status': 'Pending Authentication',
            'authenticated': False
        }
        
        self.authenticated_devices.append(device_info)
        self.update_device_list()
        self.device_id_input.clear()

    def select_device(self, item):
        """Select a device from the list"""
        self.selected_device_index = self.device_list_widget.row(item)

    def authenticate_device(self):
        """Authenticate the selected device"""
        if self.selected_device_index < 0:
            QMessageBox.warning(self, "Selection Required", "Please select a device to authenticate")
            return
        
        auth_key = self.auth_key_input.text().strip()
        if not auth_key:
            QMessageBox.warning(self, "Input Error", "Please enter an authentication key")
            return
        
        device = self.authenticated_devices[self.selected_device_index]
        
        # Simulate authentication (replace with actual IOT device authentication)
        try:
            # Here you would implement actual IOT device authentication
            # For now, we'll simulate a successful authentication
            device['authenticated'] = True
            device['status'] = 'Authenticated'
            device['auth_key'] = auth_key
            
            self.update_device_list()
            self.auth_key_input.clear()
            QMessageBox.information(self, "Success", f"Device {device['id']} authenticated successfully")
            
            # Emit signal to update other components
            self.devices_updated.emit(self.authenticated_devices)
            
        except Exception as e:
            QMessageBox.critical(self, "Authentication Failed", f"Failed to authenticate device: {str(e)}")

    def test_device_connection(self):
        """Test connection to selected device"""
        if self.selected_device_index < 0:
            QMessageBox.warning(self, "Selection Required", "Please select a device to test")
            return
        
        device = self.authenticated_devices[self.selected_device_index]
        
        if not device.get('authenticated', False):
            QMessageBox.warning(self, "Authentication Required", "Device must be authenticated first")
            return
        
        # Simulate connection test (replace with actual IOT device connection test)
        import random
        if random.choice([True, False]):
            QMessageBox.information(self, "Connection Test", f"Successfully connected to {device['id']}")
        else:
            QMessageBox.warning(self, "Connection Test", f"Failed to connect to {device['id']}")

    def remove_selected_device(self):
        """Remove selected device from list"""
        if self.selected_device_index < 0:
            QMessageBox.warning(self, "Selection Required", "Please select a device to remove")
            return
        
        device = self.authenticated_devices[self.selected_device_index]
        reply = QMessageBox.question(self, "Confirm Removal", 
                                   f"Are you sure you want to remove {device['id']}?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            removed_device = self.authenticated_devices.pop(self.selected_device_index)
            self.update_device_list()
            self.selected_device_index = -1
            
            # Emit signal to update other components
            self.devices_updated.emit(self.authenticated_devices)

    def update_device_list(self):
        """Update the device list widget"""
        self.device_list_widget.clear()
        for device in self.authenticated_devices:
            status_icon = "✅" if device.get('authenticated', False) else "⏳"
            item_text = f"{status_icon} {device['id']} ({device['type']}) - {device['status']}"
            self.device_list_widget.addItem(item_text)

    def restore_cached_devices(self):
        """Restore cached devices from settings"""
        cached_devices = self.settings.value("iot_authenticated_devices", [])
        if cached_devices:
            self.authenticated_devices = cached_devices
            self.update_device_list()

    def save_devices(self):
        """Save devices to settings"""
        self.settings.setValue("iot_authenticated_devices", self.authenticated_devices)

    def get_authenticated_devices(self):
        """Get list of authenticated devices"""
        return [d for d in self.authenticated_devices if d.get('authenticated', False)] 