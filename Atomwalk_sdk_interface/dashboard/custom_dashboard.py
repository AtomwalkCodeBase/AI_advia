# dashboard/custom_dashboard.py - Custom SDK Dashboard

from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QLineEdit, QFormLayout
from PyQt5.QtCore import Qt

class CustomConfigTab(QWidget):
    """Custom Configuration Tab"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 500)
        self.setStyleSheet("font-size: 15px;")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Custom SDK Configuration")
        header.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(header)
        
        # Custom configuration form
        form_layout = QFormLayout()
        
        self.api_endpoint = QLineEdit()
        self.api_endpoint.setPlaceholderText("Enter API endpoint")
        form_layout.addRow("API Endpoint:", self.api_endpoint)
        
        self.device_type = QLineEdit()
        self.device_type.setPlaceholderText("Enter device type")
        form_layout.addRow("Device Type:", self.device_type)
        
        self.config_file = QLineEdit()
        self.config_file.setPlaceholderText("Path to configuration file")
        form_layout.addRow("Config File:", self.config_file)
        
        layout.addLayout(form_layout)
        
        # Configuration description
        desc = QLabel("Custom SDK Configuration\n\nConfigure your custom SDK settings, API endpoints, and device specifications.")
        desc.setStyleSheet("font-size: 14px; color: #666; margin-top: 20px;")
        layout.addWidget(desc)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Configuration")
        save_btn.setStyleSheet("background-color: #0078d4; color: white; padding: 10px;")
        
        load_btn = QPushButton("Load Configuration")
        load_btn.setStyleSheet("background-color: #107c10; color: white; padding: 10px;")
        
        test_btn = QPushButton("Test Connection")
        test_btn.setStyleSheet("background-color: #d83b01; color: white; padding: 10px;")
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(load_btn)
        button_layout.addWidget(test_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        self.setLayout(layout)

class CustomLogsTab(QWidget):
    """Custom Logs Tab"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 500)
        self.setStyleSheet("font-size: 15px;")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Custom SDK Logs")
        header.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(header)
        
        # Log viewer
        self.log_viewer = QTextEdit()
        self.log_viewer.setPlaceholderText("Custom SDK logs will appear here...")
        self.log_viewer.setStyleSheet("font-family: 'Courier New'; font-size: 12px;")
        layout.addWidget(self.log_viewer)
        
        # Log controls
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh Logs")
        refresh_btn.setStyleSheet("background-color: #0078d4; color: white; padding: 8px;")
        
        clear_btn = QPushButton("Clear Logs")
        clear_btn.setStyleSheet("background-color: #d83b01; color: white; padding: 8px;")
        
        export_btn = QPushButton("Export Logs")
        export_btn.setStyleSheet("background-color: #107c10; color: white; padding: 8px;")
        
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(export_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

class Custom_Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atomwalk Custom SDK Dashboard")
        self.setMinimumSize(1000, 700)

        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # Custom-specific tabs
        self.custom_config_tab = CustomConfigTab()
        self.custom_logs_tab = CustomLogsTab()

        self.tab_widget.addTab(self.custom_config_tab, "Configuration")
        self.tab_widget.addTab(self.custom_logs_tab, "Logs")

        layout.addWidget(self.tab_widget)
        self.setLayout(layout) 