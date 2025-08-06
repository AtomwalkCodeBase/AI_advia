# main.py - Updated to match expense claim API format
from .sensor_reader import read_sensor
from .formatter import format_data
from .sender import send_to_erp
from .config import EMP_ID
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def start_sdk(is_edit_mode=False, claim_id=None, master_claim_id=None, project_id=None):
    """
    Start the IOT SDK to send sensor data as expense claims
    
    Args:
        is_edit_mode: Whether this is an edit operation
        claim_id: Claim ID for updates
        master_claim_id: Master claim ID for additions
        project_id: Project ID (optional)
    """
    try:
        logging.info("🔍 Reading sensor data...")
        data = read_sensor()

        logging.info("📝 Formatting data for expense claim API...")
        formatted = format_data(
            data, 
            EMP_ID, 
            is_edit_mode=is_edit_mode,
            claim_id=claim_id,
            master_claim_id=master_claim_id,
            project_id=project_id
        )

        logging.info("📤 Sending data to expense claim API...")
        response = send_to_erp(formatted)

        if response:
            logging.info(f"✅ Expense claim submitted successfully: {response}")
            return True
        else:
            logging.error("❌ Failed to submit expense claim")
            return False
    except Exception as e:
        logging.error(f"❌ Error in IOT SDK: {e}")
        return False

def submit_new_claim(project_id=None, master_claim_id=None):
    """Submit a new expense claim with sensor data"""
    return start_sdk(
        is_edit_mode=False,
        master_claim_id=master_claim_id,
        project_id=project_id
    )

def update_existing_claim(claim_id, project_id=None):
    """Update an existing expense claim with sensor data"""
    return start_sdk(
        is_edit_mode=True,
        claim_id=claim_id,
        project_id=project_id
    )

# ✅ Make sure this part exists!
if __name__ == "__main__":
    # Example usage
    print("🚀 Starting IOT SDK for expense claim submission...")
    success = start_sdk()
    if success:
        print("✅ SDK completed successfully!")
    else:
        print("❌ SDK encountered an error!")
