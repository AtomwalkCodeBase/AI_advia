import json
import os
from PyQt5.QtCore import QSettings

def sync_proxy_config_with_settings():
    """
    Sync the advia_proxy/config.json file with QSettings values.
    This ensures both the proxy listener and SDK use the same TCP/IP settings.
    """
    try:
        # Get settings from QSettings
        settings = QSettings("Atomwalk", "LogInApp")
        tcp_ip = settings.value("tcp_ip", "127.0.0.1")
        tcp_port = int(settings.value("tcp_port", 9200))
        
        # Path to proxy config file
        config_path = "C:/Users/WIN11 24H2/Desktop/Atomwalk/Advia_Interface/advia_proxy/config.json"
        
        # Check if config file exists
        if not os.path.exists(config_path):
            print(f"Proxy config file not found: {config_path}")
            return False
        
        # Read current config
        with open(config_path, "r") as f:
            config = json.load(f)
        
        # Update TCP settings
        config["tcp_ip"] = tcp_ip
        config["tcp_port"] = tcp_port
        
        # Determine connection mode based on what's in QSettings
        # If TCP settings are set, use TCP mode
        if tcp_ip and tcp_port:
            config["connection_mode"] = "tcp"
        
        # Write updated config back to file
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Proxy config synced: TCP {tcp_ip}:{tcp_port}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to sync proxy config: {e}")
        return False

def get_current_tcp_settings():
    """
    Get current TCP settings from QSettings.
    Returns tuple of (ip, port) or (None, None) if not set.
    """
    settings = QSettings("Atomwalk", "LogInApp")
    tcp_ip = settings.value("tcp_ip", "")
    tcp_port = settings.value("tcp_port", "")
    
    if tcp_ip and tcp_port:
        return tcp_ip, int(tcp_port)
    return None, None

def check_config_sync():
    """
    Check if proxy config.json matches QSettings.
    Returns True if in sync, False otherwise.
    """
    try:
        # Get QSettings values
        settings = QSettings("Atomwalk", "LogInApp")
        qsettings_ip = settings.value("tcp_ip", "")
        qsettings_port = settings.value("tcp_port", "")
        
        # Get config.json values
        config_path = "C:/Users/WIN11 24H2/Desktop/Atomwalk/Advia_Interface/advia_proxy/config.json"
        if not os.path.exists(config_path):
            return False
            
        with open(config_path, "r") as f:
            config = json.load(f)
        
        config_ip = config.get("tcp_ip", "")
        config_port = config.get("tcp_port", "")
        
        # Compare values
        return (qsettings_ip == config_ip and 
                str(qsettings_port) == str(config_port))
        
    except Exception as e:
        print(f"Error checking config sync: {e}")
        return False 