from PyQt5.QtWidgets import QApplication
from Atomwalk_sdk_interface.ui.login import LoginWindow
from Atomwalk_sdk_interface.dashboard.main_dashboard import MainDashboard
from SDK.scripts.main import start_sdk
from advia_proxy.proxy_listener import activate_proxy
import sys
import traceback

class SDKInterfaceApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = None
        self.main_dashboard = None

    def run(self):
        print("🚀 Application started")
        self.show_login()
        sys.exit(self.app.exec_())

    def show_login(self):
        self.login_window = LoginWindow(on_login_success=self.on_login_success)
        self.login_window.show()

    def on_login_success(self):
        print("✅ Login successful! Attempting to start SDK...")

        try:
            # 🔁 Step 1: Trigger the SDK
            sdk_status = start_sdk()

            if sdk_status:
                print("✅ SDK started successfully. System is ready.")
            else:
                # ❌ SDK failed: Fallback to Proxy
                print("⚠️ SDK failed or returned inactive status.")
                self.trigger_proxy_listener()

        except Exception as e:
            print("❌ Exception while starting SDK:")
            print(traceback.format_exc())
            self.trigger_proxy_listener()

        # ✅ Step 2: Always load the dashboard
        self.main_dashboard = MainDashboard()
        self.main_dashboard.show()

    def trigger_proxy_listener(self):
        """
        Handles fallback when SDK is unavailable.
        """
        try:
            print("🛡️ Activating Proxy Listener (Backup Mode)...")
            activate_proxy()
            print("📂 Proxy is in standby for manual file drop or backup modes.")
        except Exception as proxy_error:
            print(f"❌ Failed to activate Proxy Listener: {proxy_error}")

if __name__ == "__main__":
    sdk_app = SDKInterfaceApp()
    sdk_app.run()
