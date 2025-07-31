# dashboard/iot_dashboard.py - IOT Devices SDK Dashboard

from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class IOTDevicesTab(QWidget):
    """IOT Devices Management Tab"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 500)
        self.setStyleSheet("font-size: 15px;")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("IOT Devices Management")
        header.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(header)
        
        # IOT-specific content
        content = QLabel("IOT Devices SDK - Device Management Interface\n\nThis interface allows you to manage IOT devices, configure sensors, and monitor device status.")
        content.setStyleSheet("font-size: 14px; color: #666;")
        content.setAlignment(Qt.AlignCenter)
        layout.addWidget(content)
        
        # Placeholder buttons for IOT functionality
        button_layout = QHBoxLayout()
        
        scan_btn = QPushButton("Scan IOT Devices")
        scan_btn.setStyleSheet("background-color: #0078d4; color: white; padding: 10px;")
        
        config_btn = QPushButton("Configure Sensors")
        config_btn.setStyleSheet("background-color: #107c10; color: white; padding: 10px;")
        
        monitor_btn = QPushButton("Device Monitor")
        monitor_btn.setStyleSheet("background-color: #d83b01; color: white; padding: 10px;")
        
        button_layout.addWidget(scan_btn)
        button_layout.addWidget(config_btn)
        button_layout.addWidget(monitor_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        self.setLayout(layout)

class IOTStatusTab(QWidget):
    """IOT Status Monitoring Tab"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 500)
        self.setStyleSheet("font-size: 15px;")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("IOT Status Monitor")
        header.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(header)
        
        # IOT status content
        content = QLabel("IOT Devices SDK - Status Monitoring\n\nMonitor real-time status of IOT devices, sensor readings, and system health.")
        content.setStyleSheet("font-size: 14px; color: #666;")
        content.setAlignment(Qt.AlignCenter)
        layout.addWidget(content)
        
        # Placeholder for IOT status monitoring
        status_label = QLabel("🟢 System Status: Online\n📊 Active Devices: 0\n📡 Sensor Readings: No data")
        status_label.setStyleSheet("font-size: 16px; background-color: #f0f0f0; padding: 20px; border-radius: 10px;")
        status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(status_label)
        
        layout.addStretch()
        self.setLayout(layout)

class IOT_Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atomwalk IOT Devices SDK Dashboard")
        self.setMinimumSize(1000, 700)

        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # IOT-specific tabs
        self.iot_devices_tab = IOTDevicesTab()
        self.iot_status_tab = IOTStatusTab()

        self.tab_widget.addTab(self.iot_devices_tab, "IOT Devices")
        self.tab_widget.addTab(self.iot_status_tab, "Status Monitor")

        layout.addWidget(self.tab_widget)
        self.setLayout(layout) 