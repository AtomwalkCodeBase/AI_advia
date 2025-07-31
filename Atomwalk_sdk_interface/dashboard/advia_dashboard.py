# dashboard/advia_dashboard.py - ADVIA SDK Dashboard

from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from Atomwalk_sdk_interface.ui.device_tab import DeviceTab
from Atomwalk_sdk_interface.ui.status_tab import StatusTab
from Atomwalk_sdk_interface.ui.processed_files_tab import ProcessedFilesTab

class ADVIA_Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atomwalk ADVIA SDK Dashboard")
        self.setMinimumSize(1000, 700)

        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # ADVIA-specific tabs
        self.device_tab = DeviceTab()
        self.status_tab = StatusTab()
        self.processed_files_tab = ProcessedFilesTab()

        # Connect signal to method
        self.device_tab.devices_updated.connect(self.status_tab.set_devices)

        self.tab_widget.addTab(self.device_tab, "Device Setup")
        self.tab_widget.addTab(self.status_tab, "Test Monitor")
        self.tab_widget.addTab(self.processed_files_tab, "Processed Files")

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        # Initial trigger
        self.status_tab.set_devices(self.device_tab.get_logged_devices()) 