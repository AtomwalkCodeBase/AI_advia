from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFrame, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap

class SDKSelectionWindow(QWidget):
    sdk_selected = pyqtSignal(str)  # Signal emitted when SDK is selected
    
    def __init__(self, on_sdk_selected, parent=None):
        super().__init__(parent)
        self.on_sdk_selected = on_sdk_selected
        self.selected_sdk = None
        
        self.setWindowTitle("Select SDK")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.showFullScreen()
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 20px;
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                min-height: 120px;
            }
            QPushButton:hover {
                background-color: #f8f8f8;
                border-color: #0078d4;
            }
            QPushButton:pressed {
                background-color: #e6f3ff;
                border-color: #0078d4;
            }
            QPushButton[selected="true"] {
                background-color: #e6f3ff;
                border-color: #0078d4;
                color: #0078d4;
            }
        """)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Choose Your SDK")
        header.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #0078d4;
            margin: 20px;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Subtitle
        subtitle = QLabel("Select the SDK you want to use for this session")
        subtitle.setStyleSheet("""
            font-size: 18px;
            color: #666666;
            margin-bottom: 30px;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # SDK Options Grid
        sdk_grid = QGridLayout()
        sdk_grid.setSpacing(20)
        
        # SDK Option 1: ADVIA SDK
        self.advia_btn = QPushButton("ADVIA SDK\n\nAdvanced device integration\nfor ADVIA analyzers")
        self.advia_btn.setProperty("selected", False)
        self.advia_btn.clicked.connect(lambda: self.select_sdk("ADVIA"))
        sdk_grid.addWidget(self.advia_btn, 0, 0)
        
        # SDK Option 2: Generic SDK
        self.generic_btn = QPushButton("Generic SDK\n\nUniversal device support\nfor various analyzers")
        self.generic_btn.setProperty("selected", False)
        self.generic_btn.clicked.connect(lambda: self.select_sdk("GENERIC"))
        sdk_grid.addWidget(self.generic_btn, 0, 1)
        
        # SDK Option 3: Custom SDK
        self.custom_btn = QPushButton("Custom SDK\n\nCustom configuration\nfor specific requirements")
        self.custom_btn.setProperty("selected", False)
        self.custom_btn.clicked.connect(lambda: self.select_sdk("CUSTOM"))
        sdk_grid.addWidget(self.custom_btn, 1, 0)
        
        # SDK Option 4: Test Mode
        self.test_btn = QPushButton("Test Mode\n\nDevelopment and testing\nenvironment")
        self.test_btn.setProperty("selected", False)
        self.test_btn.clicked.connect(lambda: self.select_sdk("TEST"))
        sdk_grid.addWidget(self.test_btn, 1, 1)
        
        layout.addLayout(sdk_grid)
        
        # Continue Button
        self.continue_btn = QPushButton("Continue with Selected SDK")
        self.continue_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 18px;
                font-weight: bold;
                margin-top: 30px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.continue_btn.clicked.connect(self.continue_with_sdk)
        self.continue_btn.setEnabled(False)
        layout.addWidget(self.continue_btn, alignment=Qt.AlignCenter)
        
        # Cancel Button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666666;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        cancel_btn.clicked.connect(self.close)
        layout.addWidget(cancel_btn, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        
    def select_sdk(self, sdk_name):
        """Handle SDK selection"""
        # Clear previous selection
        for btn in [self.advia_btn, self.generic_btn, self.custom_btn, self.test_btn]:
            btn.setProperty("selected", False)
            btn.setStyleSheet(btn.styleSheet())
        
        # Set new selection
        if sdk_name == "ADVIA":
            self.advia_btn.setProperty("selected", True)
        elif sdk_name == "GENERIC":
            self.generic_btn.setProperty("selected", True)
        elif sdk_name == "CUSTOM":
            self.custom_btn.setProperty("selected", True)
        elif sdk_name == "TEST":
            self.test_btn.setProperty("selected", True)
        
        # Update button styles
        for btn in [self.advia_btn, self.generic_btn, self.custom_btn, self.test_btn]:
            btn.setStyleSheet(btn.styleSheet())
        
        self.selected_sdk = sdk_name
        self.continue_btn.setEnabled(True)
        
    def continue_with_sdk(self):
        """Continue with the selected SDK"""
        if not self.selected_sdk:
            QMessageBox.warning(self, "No SDK Selected", "Please select an SDK to continue.")
            return
            
        # Store the selected SDK in settings
        from PyQt5.QtCore import QSettings
        settings = QSettings("Atomwalk", "LogInApp")
        settings.setValue("selected_sdk", self.selected_sdk)
        
        # Emit signal and close
        self.sdk_selected.emit(self.selected_sdk)
        self.on_sdk_selected(self.selected_sdk)
        self.close() 