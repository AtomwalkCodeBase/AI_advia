from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QLineEdit, QDateEdit
)
from PyQt5.QtCore import Qt, QTimer, QDate
from Atomwalk_sdk_interface.utils.logger import fetch_logs_for_device, fetch_logs_for_device_on_date


class StatusTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 500)
        self.setStyleSheet("font-size: 15px;")
        self.devices = []

        self.init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_status)
        self.timer.start(5000)

    def init_ui(self):
        layout = QVBoxLayout()

        header = QLabel("Test Results Monitor")
        header.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(header)

        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Device ID or Test Name")
        self.search_input.textChanged.connect(self.refresh_status)

        self.date_picker = QDateEdit()
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.dateChanged.connect(self.refresh_status)

        self.refresh_button = QPushButton("Manual Refresh")
        self.refresh_button.clicked.connect(self.refresh_status)

        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.date_picker)
        filter_layout.addWidget(self.refresh_button)
        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Device ID", "Test Name", "Status", "Remarks"])
        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def set_devices(self, device_list):
        self.devices = device_list
        self.refresh_status()

    def refresh_status(self):
        self.table.setRowCount(0)
        if not self.devices:
            return

        search_text = self.search_input.text().strip().lower()
        selected_date = self.date_picker.date().toString("yyyy-MM-dd")

        for device in self.devices:
            device_id = device.get("device_id")
            logs = fetch_logs_for_device_on_date(device_id, selected_date)

            for log in logs:
                timestamp, dev_id, test_name, status, remarks = log[1], log[2], log[4], log[3], log[5]

                # Apply search filter
                if search_text and (search_text not in dev_id.lower() and search_text not in test_name.lower()):
                    continue

                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(timestamp))
                self.table.setItem(row_position, 1, QTableWidgetItem(dev_id))
                self.table.setItem(row_position, 2, QTableWidgetItem(test_name))
                self.table.setItem(row_position, 3, QTableWidgetItem(status))
                self.table.setItem(row_position, 4, QTableWidgetItem(remarks))
