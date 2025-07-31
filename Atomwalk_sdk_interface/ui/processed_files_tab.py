from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QLineEdit, QHeaderView, QMenu, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, QFileInfo
import os
from pathlib import Path

class ProcessedFilesTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 500)
        self.setStyleSheet("font-size: 15px;")
        
        # Path to processed files folder
        self.processed_dir = Path("C:/Users/WIN11 24H2/Desktop/Atomwalk/Advia_Interface/SDK/processed_to_ERP")
        
        self.init_ui()
        
        # Auto-refresh every 30 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_files)
        self.timer.start(30000)  # 30 seconds
        
        # Initial load
        self.refresh_files()

    def init_ui(self):
        layout = QVBoxLayout()

        # Header
        header = QLabel("Processed Files Monitor")
        header.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(header)

        # Filter controls
        filter_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by filename...")
        self.search_input.textChanged.connect(self.apply_filter)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_files)
        
        self.open_folder_button = QPushButton("Open Folder")
        self.open_folder_button.clicked.connect(self.open_processed_folder)
        
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.refresh_button)
        filter_layout.addWidget(self.open_folder_button)
        layout.addLayout(filter_layout)

        # Files table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Filename", "Size (KB)", "Date Modified", "Date Created", "Status"
        ])
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Filename stretches
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Size
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Modified
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Created
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Status

        # Enable context menu
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def show_context_menu(self, position):
        """Show context menu on right-click"""
        row = self.table.rowAt(position.y())
        if row >= 0:
            # Get the filename from the selected row
            filename_item = self.table.item(row, 0)
            if filename_item:
                filename = filename_item.text()
                
                # Create context menu
                context_menu = QMenu(self)
                delete_action = context_menu.addAction("Delete File")
                
                # Show menu and handle action
                action = context_menu.exec_(self.table.mapToGlobal(position))
                
                if action == delete_action:
                    self.delete_file(filename, row)

    def delete_file(self, filename, row):
        """Delete the selected file"""
        file_path = self.processed_dir / filename
        
        # Confirmation dialog
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete '{filename}'?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                if file_path.exists():
                    file_path.unlink()  # Delete the file
                    self.table.removeRow(row)  # Remove from table
                    QMessageBox.information(
                        self, 
                        "Success", 
                        f"File '{filename}' has been deleted successfully."
                    )
                else:
                    QMessageBox.warning(
                        self, 
                        "File Not Found", 
                        f"File '{filename}' no longer exists."
                    )
                    self.refresh_files()  # Refresh to update the list
                    
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "Error", 
                    f"Failed to delete file '{filename}':\n{str(e)}"
                )

    def refresh_files(self):
        """Load and display all files from the processed directory"""
        self.table.setRowCount(0)
        
        if not self.processed_dir.exists():
            self.add_info_row("Processed directory not found", "Error", "Directory does not exist")
            return
        
        try:
            files = [f for f in self.processed_dir.iterdir() if f.is_file()]
            
            if not files:
                self.add_info_row("No processed files found", "Info", "Directory is empty")
                return
            
            for file_path in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True):
                self.add_file_row(file_path)
                
        except Exception as e:
            self.add_info_row(f"Error reading directory: {str(e)}", "Error", "Access denied")

    def add_file_row(self, file_path):
        """Add a file to the table"""
        try:
            file_info = QFileInfo(str(file_path))
            
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            # Filename
            self.table.setItem(row_position, 0, QTableWidgetItem(file_path.name))
            
            # Size in KB
            size_kb = file_info.size() / 1024
            size_text = f"{size_kb:.1f}" if size_kb > 0 else "0"
            self.table.setItem(row_position, 1, QTableWidgetItem(size_text))
            
            # Date Modified
            modified_date = file_info.lastModified().toString("yyyy-MM-dd hh:mm:ss")
            self.table.setItem(row_position, 2, QTableWidgetItem(modified_date))
            
            # Date Created
            created_date = file_info.birthTime().toString("yyyy-MM-dd hh:mm:ss")
            self.table.setItem(row_position, 3, QTableWidgetItem(created_date))
            
            # Status (based on file extension)
            status = "Processed" if file_path.suffix.lower() == '.astm' else "Other"
            self.table.setItem(row_position, 4, QTableWidgetItem(status))
            
        except Exception as e:
            print(f"Error adding file row: {e}")

    def add_info_row(self, message, status, details):
        """Add an informational row to the table"""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        self.table.setItem(row_position, 0, QTableWidgetItem(message))
        self.table.setItem(row_position, 1, QTableWidgetItem(""))
        self.table.setItem(row_position, 2, QTableWidgetItem(""))
        self.table.setItem(row_position, 3, QTableWidgetItem(""))
        self.table.setItem(row_position, 4, QTableWidgetItem(status))

    def apply_filter(self):
        """Filter table rows based on search text"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.table.rowCount()):
            filename_item = self.table.item(row, 0)
            if filename_item:
                filename = filename_item.text().lower()
                self.table.setRowHidden(row, search_text not in filename)

    def open_processed_folder(self):
        """Open the processed files folder in file explorer"""
        try:
            import subprocess
            if self.processed_dir.exists():
                subprocess.run(['explorer', str(self.processed_dir)])
            else:
                print("Processed directory does not exist")
        except Exception as e:
            print(f"Error opening folder: {e}") 