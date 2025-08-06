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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #ffffff;
            }
            
            QLabel {
                color: #ffffff;
                background: transparent;
            }
            
            QPushButton {
                background: rgba(255, 255, 255, 0.95);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                padding: 25px;
                font-size: 16px;
                font-weight: 600;
                color: #2c3e50;
                min-height: 120px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            }
            
            QPushButton:hover {
                background: rgba(255, 255, 255, 1.0);
                border-color: #3498db;
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            }
            
            QPushButton:pressed {
                background: rgba(52, 152, 219, 0.1);
                border-color: #2980b9;
                transform: translateY(0px);
            }
            
            QPushButton[selected="true"] {
                background: rgba(255, 255, 255, 1);
                border-color: #3498db;
                color: #2980b9;
                box-shadow: 0 8px 25px rgba(52, 152, 219, 0.3);
            }
            
            QPushButton[selected="true"]:hover {
                background: rgba(52, 152, 219, 0.2);
                border-color: #2980b9;
            }
        """)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(30)
        
        # Header
        header = QLabel("🚀 Choose Your SDK")
        header.setStyleSheet("""
            font-size: 42px;
            font-weight: 700;
            color: #ffffff;
            margin: 30px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            background: transparent;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Subtitle
        subtitle = QLabel("Select the SDK you want to use for this session")
        subtitle.setStyleSheet("""
            font-size: 20px;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 40px;
            background: transparent;
            font-weight: 300;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # SDK Options Grid
        sdk_grid = QGridLayout()
        sdk_grid.setSpacing(25)
        sdk_grid.setContentsMargins(40, 20, 40, 20)
        
        # SDK Option 1: ADVIA SDK
        self.advia_btn = QPushButton("🔬 ADVIA SDK\n\nAdvanced device integration\nfor ADVIA analyzers\n\n• Device Authentication\n• Test Monitor\n• Proxy Listener")
        self.advia_btn.setProperty("selected", False)
        self.advia_btn.clicked.connect(lambda: self.select_sdk("ADVIA"))
        sdk_grid.addWidget(self.advia_btn, 0, 0)
        
        # SDK Option 2: IOT SDK
        self.generic_btn = QPushButton("🌐 IOT SDK\n\nUniversal device support\nfor various IOT devices\n\n• Device Authentication\n• Real-time Monitoring\n• Sensor Management")
        self.generic_btn.setProperty("selected", False)
        self.generic_btn.clicked.connect(lambda: self.select_sdk("IOT_SDK"))
        sdk_grid.addWidget(self.generic_btn, 0, 1)
        
        # SDK Option 3: Custom SDK
        self.custom_btn = QPushButton("⚙️ Custom SDK\n\nCustom configuration\nfor specific requirements\n\n• Flexible Setup\n• Custom Protocols\n• Advanced Options")
        self.custom_btn.setProperty("selected", False)
        self.custom_btn.clicked.connect(lambda: self.select_sdk("CUSTOM"))
        sdk_grid.addWidget(self.custom_btn, 1, 0)
        
        # SDK Option 4: Test Mode
        self.test_btn = QPushButton("🧪 Test Mode\n\nDevelopment and testing\nenvironment\n\n• Debug Tools\n• Simulation Mode\n• Testing Interface")
        self.test_btn.setProperty("selected", False)
        self.test_btn.clicked.connect(lambda: self.select_sdk("TEST"))
        sdk_grid.addWidget(self.test_btn, 1, 1)
        
        layout.addLayout(sdk_grid)
        
        # Continue Button
        self.continue_btn = QPushButton("✅ Continue with Selected SDK")
        self.continue_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #27ae60, stop:1 #2ecc71);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 40px;
                font-size: 18px;
                font-weight: 600;
                margin-top: 40px;
                box-shadow: 0 4px 15px rgba(39, 174, 96, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #229954, stop:1 #27ae60);
                box-shadow: 0 6px 20px rgba(39, 174, 96, 0.4);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e8449, stop:1 #229954);
                transform: translateY(0px);
            }
            QPushButton:disabled {
                background: rgba(255, 255, 255, 0.3);
                color: rgba(255, 255, 255, 0.6);
                box-shadow: none;
            }
        """)
        self.continue_btn.clicked.connect(self.continue_with_sdk)
        self.continue_btn.setEnabled(False)
        layout.addWidget(self.continue_btn, alignment=Qt.AlignCenter)
        
        # Cancel Button
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: rgba(231, 76, 60, 0.9);
                color: white;
                border: 2px solid rgba(231, 76, 60, 0.8);
                border-radius: 12px;
                padding: -10px 50px;
                font-size: 16px;
                font-weight: 600;
                margin-top: 0px;
                box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
                height:0px;

            }
            QPushButton:hover {
                background: rgba(231, 76, 60, 1.0);
                border-color: rgba(231, 76, 60, 1.0);
                box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: rgba(192, 57, 43, 1.0);
                border-color: rgba(192, 57, 43, 1.0);
                transform: translateY(0px);
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
        elif sdk_name == "IOT_SDK":
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