import socket
import threading
import requests
import keyboard
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer, QSettings


CLOUD_LOGIN_API = "https://crm.atomwalk.com/rest-auth/login/"
FORCED_LOGIN_INTERVAL = 60 * 60 * 1000  # 1 hour


def validate_login(username, password):
    try:
        response = requests.post(CLOUD_LOGIN_API, json={'username': username, 'password': password})
        if response.status_code == 200:
            return response.json().get("key")
        else:
            print("Login failed:", response.status_code, response.text)
    except requests.ConnectionError:
        return 1
    except Exception as e:
        print(f"Error validating login: {e}")
    return False


def send_login_info(username, token, is_active=True):
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
    }
    data = {
        "name": username,
        "host_name": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        'is_active': is_active
    }

    db_name = username.split('@')[-1]
    CLOUD_TRACKING_API = f"https://crm.atomwalk.com/api/external_login_info/{db_name}/"

    try:
        response = requests.post(CLOUD_TRACKING_API, json=data, headers=headers)
        return True
    except Exception as e:
        print("Login info error:", e)
        return False


class LoginWindow(QMainWindow):
    def __init__(self, on_login_success, parent=None):
        super().__init__(parent)
        self.on_login_success = on_login_success
        self.settings = QSettings("Atomwalk", "LogInApp")
        self.setWindowTitle("User Login")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.showFullScreen()
        self.init_ui()

        self.relogin_timer = QTimer(self)
        self.relogin_timer.timeout.connect(self.show_login_screen)
        self.relogin_timer.start(FORCED_LOGIN_INTERVAL)

        threading.Thread(target=self.listen_for_hotkey, daemon=True).start()
        self.update_button_visibility()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addStretch()

        self.label = QLabel("Enter Username & Password:")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedSize(450, 40)
        self.username_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.username_input, alignment=Qt.AlignCenter)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedSize(450, 40)
        self.password_input.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()

        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("font-size: 16px; background-color: blue; color: white;")
        self.login_button.setFixedSize(150, 40)
        self.login_button.clicked.connect(self.check_login)
        button_layout.addWidget(self.login_button)

        self.continue_button = QPushButton("Continue")
        self.continue_button.setStyleSheet("font-size: 16px;")
        self.continue_button.setFixedSize(150, 40)
        self.continue_button.clicked.connect(self.continue_with_token)
        button_layout.addWidget(self.continue_button)

        self.logout_button = QPushButton("Logout")
        self.logout_button.setStyleSheet("font-size: 16px; background-color: red; color: white;")
        self.logout_button.setFixedSize(150, 40)
        self.logout_button.clicked.connect(self.logout)
        button_layout.addWidget(self.logout_button)

        layout.addLayout(button_layout)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_button_visibility(self):
        stored_token = self.settings.value("auth_token", "")
        if stored_token and stored_token != "1":
            self.login_button.hide()
            self.continue_button.show()
            self.logout_button.show()
            self.password_input.hide()
            self.username_input.show()  # Show username field for continue
        else:
            self.login_button.show()
            self.password_input.show()
            self.username_input.show()
            self.continue_button.hide()
            self.logout_button.hide()

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        token = validate_login(username, password)

        if token:
            if token == 1:
                self.label.setText("No Internet. Continue without login.")
                self.settings.setValue("auth_token", token)
            else:
                send_login_info(username, token)
                self.settings.setValue("auth_token", token)
                self.settings.setValue("user_name", username)
                self.on_login_success()
                self.close()
        else:
            self.label.setText("Invalid credentials.")

    def logout(self):
        token = self.settings.value("auth_token", "")
        user = self.settings.value("user_name", "")
        if token:
            if send_login_info(user, token, is_active=False):
                self.settings.remove("auth_token")
                self.settings.remove("user_name")
                self.username_input.clear()
                self.password_input.clear()
                self.label.setText("Enter Username & Password:")
                self.update_button_visibility()
                self.showFullScreen()

    def show_login_screen(self):
        token = self.settings.value("auth_token", "")
        self.password_input.clear()
        if token == "1":
            self.label.setText("Re-enter Credentials:")
        else:
            self.label.setText("Continue with current session or logout:")
        self.update_button_visibility()
        self.showFullScreen()

    def continue_with_token(self):
        # Require username to be entered even when token exists
        entered_username = self.username_input.text().strip()
        if not entered_username:
            self.label.setText("Please enter your username to continue.")
            return
            
        token = self.settings.value("auth_token", "")
        stored_user = self.settings.value("user_name", "")
        
        # Validate that entered username matches stored username
        if entered_username != stored_user:
            self.label.setText("Username does not match stored session. Please login again.")
            return
            
        if token:
            if token != "1":
                send_login_info(entered_username, token)
            self.on_login_success()
            self.close()
        else:
            self.label.setText("Session expired. Please login again.")

    def listen_for_hotkey(self):
        keyboard.add_hotkey("ctrl+l", self.trigger_login_screen)

    def trigger_login_screen(self):
        QTimer.singleShot(0, self.show_login_screen)
