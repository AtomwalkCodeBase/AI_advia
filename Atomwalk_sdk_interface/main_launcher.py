from PyQt5.QtWidgets import QApplication
from Atomwalk_sdk_interface.ui.login import LoginWindow
from Atomwalk_sdk_interface.ui.sdk_selection import SDKSelectionWindow
from Atomwalk_sdk_interface.dashboard.advia_dashboard import ADVIA_Dashboard
from Atomwalk_sdk_interface.dashboard.iot_dashboard import IOT_Dashboard
from Atomwalk_sdk_interface.dashboard.custom_dashboard import Custom_Dashboard
from Atomwalk_sdk_interface.dashboard.test_dashboard import Test_Dashboard
from SDK1.scripts.main import start_sdk
from IOT_SDK.main import start_sdk as start_iot_sdk
from advia_proxy.proxy_listener import activate_proxy
from Atomwalk_sdk_interface.utils.config_sync import sync_proxy_config_with_settings
import sys
import traceback

class SDKInterfaceApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = None
        self.sdk_selection_window = None
        self.main_dashboard = None

    def run(self):
        print("🚀 Application started")
        
        self.show_login()
        sys.exit(self.app.exec_())

    def show_login(self):
        self.login_window = LoginWindow(on_login_success=self.on_login_success)
        self.login_window.show()

    def on_login_success(self):
        print("✅ Login successful! Showing SDK selection...")
        self.show_sdk_selection()

    def show_sdk_selection(self):
        """Show SDK selection screen after login"""
        self.sdk_selection_window = SDKSelectionWindow(on_sdk_selected=self.on_sdk_selected)
        self.sdk_selection_window.show()

    def on_sdk_selected(self, selected_sdk):
        """Handle SDK selection and start the appropriate SDK"""
        print(f"✅ SDK selected: {selected_sdk}")
        print("🔄 Starting selected SDK...")

        try:
            # Start the appropriate SDK based on selection
            if selected_sdk == "ADVIA":
                # Sync proxy config only when ADVIA SDK is selected
                print("🔄 Syncing ADVIA proxy configuration...")
                sync_proxy_config_with_settings()
                
                # Start ADVIA SDK (your current main.py)
                sdk_status = start_sdk()
            elif selected_sdk == "IOT_SDK":
                # Start IOT SDK (from IOT_SDK folder)
                print("🌐 Starting IOT SDK for sensor data collection...")
                start_iot_sdk()
                sdk_status = True  # IOT SDK doesn't return status, assume success
            elif selected_sdk == "CUSTOM":
                # Start Custom SDK
                sdk_status = start_sdk()  # For now, using same function
            elif selected_sdk == "TEST":
                # Start Test Mode SDK
                sdk_status = start_sdk()  # For now, using same function
            else:
                sdk_status = None

            # Handle SDK status
            if sdk_status is True:
                print(f"✅ {selected_sdk} SDK started successfully. System is ready.")
            elif sdk_status is False:
                print(f"⚠️ {selected_sdk} SDK encountered issues during processing.")
                # Only ADVIA SDK can use proxy listener as fallback
                if selected_sdk == "ADVIA":
                    print("🔄 ADVIA SDK had issues, activating proxy listener as backup...")
                    self.trigger_proxy_listener()
            elif sdk_status is None:
                print(f"ℹ️ {selected_sdk} SDK found no files to process.")
                # Only ADVIA SDK can use proxy listener as fallback
                if selected_sdk == "ADVIA":
                    print("🔄 ADVIA SDK found no files, activating proxy listener for manual file drop...")
                    self.trigger_proxy_listener()
            else:
                print(f"❌ {selected_sdk} SDK failed to start.")
                # Only ADVIA SDK can use proxy listener as fallback
                if selected_sdk == "ADVIA":
                    print("🔄 ADVIA SDK failed, activating proxy listener as backup...")
                    self.trigger_proxy_listener()
                else:
                    print(f"⚠️ {selected_sdk} SDK failed. Please check your configuration.")

        except Exception as e:
            print(f"❌ Exception while starting {selected_sdk} SDK:")
            print(traceback.format_exc())
            # Handle exception based on SDK type
            if selected_sdk == "ADVIA":
                print("🔄 ADVIA SDK encountered an error, activating proxy listener as backup...")
                self.trigger_proxy_listener()
            else:
                print(f"⚠️ {selected_sdk} SDK encountered an error. Please check your setup.")

        # ✅ Load SDK-specific dashboard
        self.load_sdk_dashboard(selected_sdk)

    def load_sdk_dashboard(self, selected_sdk):
        """Load the appropriate dashboard based on selected SDK"""
        print(f"📊 Loading {selected_sdk} dashboard...")
        
        if selected_sdk == "ADVIA":
            self.main_dashboard = ADVIA_Dashboard()
        elif selected_sdk == "IOT_SDK":
            self.main_dashboard = IOT_Dashboard()
        elif selected_sdk == "CUSTOM":
            self.main_dashboard = Custom_Dashboard()
        elif selected_sdk == "TEST":
            self.main_dashboard = Test_Dashboard()
        else:
            # Fallback to ADVIA dashboard
            self.main_dashboard = ADVIA_Dashboard()
        
        self.main_dashboard.show()
        print(f"✅ {selected_sdk} dashboard loaded successfully.")

    def trigger_proxy_listener(self):
        """
        Handles fallback when ADVIA SDK is unavailable.
        Only ADVIA SDK supports proxy listener fallback.
        """
        try:
            print("🛡️ Activating ADVIA Proxy Listener (Backup Mode)...")
            activate_proxy()
            print("📂 ADVIA Proxy is in standby for manual file drop or backup modes.")
        except Exception as proxy_error:
            print(f"❌ Failed to activate ADVIA Proxy Listener: {proxy_error}")

if __name__ == "__main__":
    sdk_app = SDKInterfaceApp()
    sdk_app.run()
