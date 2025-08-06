from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QLineEdit, QDateEdit, QComboBox,
    QGroupBox
)
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QColor
import json
import random
from datetime import datetime, timedelta

class IOTStatusTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setStyleSheet("font-size: 15px;")
        self.devices = []
        self.sensor_data = {}
        self.monitoring_active = False

        self.init_ui()

        # Timer for sensor data updates
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_sensor_data)
        self.update_timer.start(3000)  # Update every 3 seconds

    def init_ui(self):
        layout = QVBoxLayout()

        # -------- Header Section --------
        header_layout = QHBoxLayout()
        
        header_label = QLabel("IOT Devices Test Monitor")
        header_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        
        self.monitoring_status = QLabel("🟢 Monitoring Active")
        self.monitoring_status.setStyleSheet("color: green; font-weight: bold;")
        
        self.toggle_monitoring_btn = QPushButton("⏸️ Pause Monitoring")
        self.toggle_monitoring_btn.clicked.connect(self.toggle_monitoring)
        
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(self.monitoring_status)
        header_layout.addWidget(self.toggle_monitoring_btn)
        
        layout.addLayout(header_layout)

        # -------- Filter Section --------
        filter_group = QGroupBox("Filter Options")
        filter_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Device ID or Sensor Type")
        self.search_input.textChanged.connect(self.refresh_status)
        
        self.device_filter = QComboBox()
        self.device_filter.addItem("All Devices")
        self.device_filter.currentTextChanged.connect(self.refresh_status)
        
        self.sensor_filter = QComboBox()
        self.sensor_filter.addItems(["All Sensors", "Temperature", "Humidity", "Pressure", "Motion"])
        self.sensor_filter.currentTextChanged.connect(self.refresh_status)
        
        self.date_picker = QDateEdit()
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.dateChanged.connect(self.refresh_status)
        
        self.refresh_button = QPushButton("🔄 Manual Refresh")
        self.refresh_button.clicked.connect(self.refresh_status)
        
        filter_layout.addWidget(QLabel("Search:"))
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(QLabel("Device:"))
        filter_layout.addWidget(self.device_filter)
        filter_layout.addWidget(QLabel("Sensor:"))
        filter_layout.addWidget(self.sensor_filter)
        filter_layout.addWidget(QLabel("Date:"))
        filter_layout.addWidget(self.date_picker)
        filter_layout.addWidget(self.refresh_button)
        
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)

        # -------- Sensor Data Table --------
        data_group = QGroupBox("Sensor Data Log")
        data_layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Timestamp", "Device ID", "Sensor Type", "Value", "Unit", "Status", "Quality"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        
        # Set column widths
        self.table.setColumnWidth(0, 150)  # Timestamp
        self.table.setColumnWidth(1, 120)  # Device ID
        self.table.setColumnWidth(2, 120)  # Sensor Type
        self.table.setColumnWidth(3, 80)   # Value
        self.table.setColumnWidth(4, 60)   # Unit
        self.table.setColumnWidth(5, 80)   # Status
        self.table.setColumnWidth(6, 80)   # Quality
        
        data_layout.addWidget(self.table)
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)

        self.setLayout(layout)

    def set_devices(self, device_list):
        """Set the list of authenticated devices"""
        self.devices = device_list
        self.update_device_filter()
        self.refresh_status()

    def update_device_filter(self):
        """Update the device filter dropdown"""
        self.device_filter.clear()
        self.device_filter.addItem("All Devices")
        
        for device in self.devices:
            if device.get('authenticated', False):
                self.device_filter.addItem(device['id'])

    def toggle_monitoring(self):
        """Toggle monitoring on/off"""
        if self.monitoring_active:
            self.monitoring_active = False
            self.monitoring_status.setText("🔴 Monitoring Paused")
            self.monitoring_status.setStyleSheet("color: red; font-weight: bold;")
            self.toggle_monitoring_btn.setText("▶️ Start Monitoring")
        else:
            self.monitoring_active = True
            self.monitoring_status.setText("🟢 Monitoring Active")
            self.monitoring_status.setStyleSheet("color: green; font-weight: bold;")
            self.toggle_monitoring_btn.setText("⏸️ Pause Monitoring")

    def update_sensor_data(self):
        """Update sensor data (called by timer)"""
        if not self.monitoring_active:
            return
        
        # Simulate sensor data updates
        for device in self.devices:
            if device.get('authenticated', False):
                self.simulate_sensor_reading(device)
        
        self.refresh_status()

    def simulate_sensor_reading(self, device):
        """Simulate sensor reading for a device"""
        device_id = device['id']
        device_type = device['type']
        
        # Generate simulated sensor data based on device type
        if "Temperature" in device_type:
            value = round(random.uniform(18.0, 28.0), 1)
            unit = "°C"
            quality = random.choice(["Good", "Excellent", "Good"])
        elif "Humidity" in device_type:
            value = round(random.uniform(40.0, 70.0), 1)
            unit = "%"
            quality = random.choice(["Good", "Excellent", "Good"])
        elif "Pressure" in device_type:
            value = round(random.uniform(1000.0, 1020.0), 1)
            unit = "hPa"
            quality = random.choice(["Good", "Excellent", "Good"])
        elif "Motion" in device_type:
            value = random.choice([0, 1])
            unit = "detected"
            quality = "Good"
        else:
            value = round(random.uniform(0, 100), 2)
            unit = "units"
            quality = "Good"
        
        # Determine status based on value ranges
        if "Temperature" in device_type:
            if value < 20 or value > 26:
                status = "Warning"
            else:
                status = "Normal"
        elif "Humidity" in device_type:
            if value < 30 or value > 80:
                status = "Warning"
            else:
                status = "Normal"
        else:
            status = "Normal"
        
        # Store sensor data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sensor_data = {
            'timestamp': timestamp,
            'device_id': device_id,
            'sensor_type': device_type,
            'value': value,
            'unit': unit,
            'status': status,
            'quality': quality
        }
        
        if device_id not in self.sensor_data:
            self.sensor_data[device_id] = []
        
        self.sensor_data[device_id].append(sensor_data)
        
        # Keep only last 100 readings per device
        if len(self.sensor_data[device_id]) > 100:
            self.sensor_data[device_id] = self.sensor_data[device_id][-100:]

    def refresh_status(self):
        """Refresh the status table"""
        self.table.setRowCount(0)
        
        search_text = self.search_input.text().strip().lower()
        selected_device = self.device_filter.currentText()
        selected_sensor = self.sensor_filter.currentText()
        selected_date = self.date_picker.date().toString("yyyy-MM-dd")
        
        # Collect all sensor data
        all_data = []
        for device_id, data_list in self.sensor_data.items():
            for data in data_list:
                # Apply filters
                if search_text and (search_text not in data['device_id'].lower() and 
                                  search_text not in data['sensor_type'].lower()):
                    continue
                
                if selected_device != "All Devices" and data['device_id'] != selected_device:
                    continue
                
                if selected_sensor != "All Sensors" and selected_sensor not in data['sensor_type']:
                    continue
                
                if not data['timestamp'].startswith(selected_date):
                    continue
                
                all_data.append(data)
        
        # Sort by timestamp (newest first)
        all_data.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Add to table
        for data in all_data[:100]:  # Limit to 100 most recent entries
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            self.table.setItem(row_position, 0, QTableWidgetItem(data['timestamp']))
            self.table.setItem(row_position, 1, QTableWidgetItem(data['device_id']))
            self.table.setItem(row_position, 2, QTableWidgetItem(data['sensor_type']))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(data['value'])))
            self.table.setItem(row_position, 4, QTableWidgetItem(data['unit']))
            self.table.setItem(row_position, 5, QTableWidgetItem(data['status']))
            self.table.setItem(row_position, 6, QTableWidgetItem(data['quality']))
            
            # Color code status
            status_item = self.table.item(row_position, 5)
            if data['status'] == "Normal":
                status_item.setBackground(QColor(200, 255, 200))  # Light green
            elif data['status'] == "Warning":
                status_item.setBackground(QColor(255, 255, 200))  # Light yellow
            else:
                status_item.setBackground(QColor(255, 200, 200))  # Light red 