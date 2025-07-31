# dashboard/test_dashboard.py - Test Mode SDK Dashboard

from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QCheckBox, QSpinBox, QFormLayout
from PyQt5.QtCore import Qt

class TestEnvironmentTab(QWidget):
    """Test Environment Configuration Tab"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 500)
        self.setStyleSheet("font-size: 15px;")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Test Environment Configuration")
        header.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(header)
        
        # Test environment settings
        form_layout = QFormLayout()
        
        self.mock_data = QCheckBox("Enable Mock Data")
        self.mock_data.setChecked(True)
        form_layout.addRow("Mock Data:", self.mock_data)
        
        self.debug_mode = QCheckBox("Enable Debug Mode")
        self.debug_mode.setChecked(True)
        form_layout.addRow("Debug Mode:", self.debug_mode)
        
        self.test_duration = QSpinBox()
        self.test_duration.setRange(1, 3600)
        self.test_duration.setValue(60)
        self.test_duration.setSuffix(" seconds")
        form_layout.addRow("Test Duration:", self.test_duration)
        
        self.error_rate = QSpinBox()
        self.error_rate.setRange(0, 100)
        self.error_rate.setValue(5)
        self.error_rate.setSuffix("%")
        form_layout.addRow("Error Rate:", self.error_rate)
        
        layout.addLayout(form_layout)
        
        # Test environment description
        desc = QLabel("Test Mode SDK - Development Environment\n\nConfigure test parameters, enable mock data, and set up debugging options for development and testing.")
        desc.setStyleSheet("font-size: 14px; color: #666; margin-top: 20px;")
        layout.addWidget(desc)
        
        # Test controls
        button_layout = QHBoxLayout()
        
        start_test_btn = QPushButton("Start Test")
        start_test_btn.setStyleSheet("background-color: #107c10; color: white; padding: 10px;")
        
        stop_test_btn = QPushButton("Stop Test")
        stop_test_btn.setStyleSheet("background-color: #d83b01; color: white; padding: 10px;")
        
        reset_btn = QPushButton("Reset Environment")
        reset_btn.setStyleSheet("background-color: #0078d4; color: white; padding: 10px;")
        
        button_layout.addWidget(start_test_btn)
        button_layout.addWidget(stop_test_btn)
        button_layout.addWidget(reset_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        self.setLayout(layout)

class TestResultsTab(QWidget):
    """Test Results and Debugging Tab"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 500)
        self.setStyleSheet("font-size: 15px;")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Test Results & Debugging")
        header.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(header)
        
        # Test results viewer
        self.results_viewer = QTextEdit()
        self.results_viewer.setPlaceholderText("Test results and debug information will appear here...")
        self.results_viewer.setStyleSheet("font-family: 'Courier New'; font-size: 12px; background-color: #f8f8f8;")
        layout.addWidget(self.results_viewer)
        
        # Test status
        status_layout = QHBoxLayout()
        
        status_label = QLabel("🟡 Test Status: Ready")
        status_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        progress_label = QLabel("Progress: 0%")
        progress_label.setStyleSheet("font-size: 14px; color: #666;")
        
        status_layout.addWidget(status_label)
        status_layout.addStretch()
        status_layout.addWidget(progress_label)
        
        layout.addLayout(status_layout)
        
        # Test controls
        button_layout = QHBoxLayout()
        
        export_btn = QPushButton("Export Results")
        export_btn.setStyleSheet("background-color: #0078d4; color: white; padding: 8px;")
        
        clear_btn = QPushButton("Clear Results")
        clear_btn.setStyleSheet("background-color: #d83b01; color: white; padding: 8px;")
        
        debug_btn = QPushButton("Debug Info")
        debug_btn.setStyleSheet("background-color: #107c10; color: white; padding: 8px;")
        
        button_layout.addWidget(export_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(debug_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

class Test_Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atomwalk Test Mode SDK Dashboard")
        self.setMinimumSize(1000, 700)

        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # Test-specific tabs
        self.test_env_tab = TestEnvironmentTab()
        self.test_results_tab = TestResultsTab()

        self.tab_widget.addTab(self.test_env_tab, "Test Environment")
        self.tab_widget.addTab(self.test_results_tab, "Test Results")

        layout.addWidget(self.tab_widget)
        self.setLayout(layout) 