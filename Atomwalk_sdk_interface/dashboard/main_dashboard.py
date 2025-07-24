# dashboard/main_dashboard.py

from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from Atomwalk_sdk_interface.ui.device_tab import DeviceTab
from Atomwalk_sdk_interface.ui.status_tab import StatusTab

class MainDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atomwalk Device SDK Dashboard")
        self.setMinimumSize(1000, 700)

        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # Tabs
        self.device_tab = DeviceTab()
        self.status_tab = StatusTab()

        # Connect signal to method
        self.device_tab.devices_updated.connect(self.status_tab.set_devices)

        self.tab_widget.addTab(self.device_tab, "Device Setup")
        self.tab_widget.addTab(self.status_tab, "Test Monitor")

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        # Initial trigger
        self.status_tab.set_devices(self.device_tab.get_logged_devices())
