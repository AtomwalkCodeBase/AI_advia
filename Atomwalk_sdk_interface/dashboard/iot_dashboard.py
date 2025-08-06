# dashboard/iot_dashboard.py - IOT Devices SDK Dashboard

from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from Atomwalk_sdk_interface.ui.iot_device_tab import IOTDeviceTab
from Atomwalk_sdk_interface.ui.iot_status_tab import IOTStatusTab

class IOT_Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atomwalk IOT Devices SDK Dashboard")
        self.setMinimumSize(1000, 700)

        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # IOT-specific tabs
        self.iot_device_tab = IOTDeviceTab()
        self.iot_status_tab = IOTStatusTab()

        # Connect signal to method
        self.iot_device_tab.devices_updated.connect(self.iot_status_tab.set_devices)

        self.tab_widget.addTab(self.iot_device_tab, "Device Authentication")
        self.tab_widget.addTab(self.iot_status_tab, "Test Monitor")

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        # Initial trigger
        self.iot_status_tab.set_devices(self.iot_device_tab.get_authenticated_devices()) 