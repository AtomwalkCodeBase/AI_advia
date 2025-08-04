
import os
import shutil
from SDK1.advia_sdk.parser import parse_astm
from SDK1.advia_sdk.formatter import format_for_erp
from SDK1.advia_sdk.sender import send_to_erp
from SDK1.advia_sdk.pull_from_backup import pull_from_proxy
from Atomwalk_sdk_interface.utils.logger import log_test_result
from SDK1.advia_sdk.config import API_ENDPOINT, get_bearer_token, INCOMING_DIR, PROCESSED_DIR

def ensure_directories():
    os.makedirs(INCOMING_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

def start_sdk():
    """
    Triggered after login: checks for .astm files in incoming directory,
    processes them, and pushes to ERP.

    Returns:
        True  - if all processed successfully
        False - if some failed
        None  - if nothing to process
    """
    # Pull files from backup folder first
    pull_from_proxy()
    
    ensure_directories()
    files = [f for f in os.listdir(INCOMING_DIR) if f.endswith(".astm")]

    if not files:
        print("ℹ️ No unprocessed .astm files found.")
        log_test_result(device_id="UNKNOWN", status="No Files", test_name="File Scan", remarks="No unprocessed .astm files found.")
        return None

    device_id = "UNKNOWN"
    try:
        with open(os.path.join(INCOMING_DIR, files[0]), "r", encoding="utf-8") as f:
            raw_data = f.read()
        parsed_entries = parse_astm(raw_data)
        if parsed_entries and isinstance(parsed_entries, list) and isinstance(parsed_entries[0], dict):
            device_id = parsed_entries[0].get('device_id', 'UNKNOWN')
    except Exception as e:
        print(f"⚠️ Could not read device ID from first file: {e}")

    print(f"📁 Found {len(files)} .astm files to process.")
    log_test_result(device_id=device_id, status="Files Found", test_name="File Scan", remarks=f"{len(files)} .astm files to process.")

    all_success = True

    for filename in files:
        file_path = os.path.join(INCOMING_DIR, filename)
        print(f"\n🔍 Processing file: {filename}")
        log_test_result(device_id=device_id, status="Processing", test_name=filename, remarks="Processing file")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            parsed_entries = parse_astm(content)
            payloads = [format_for_erp(entry) for entry in parsed_entries]

            sent_all_payloads = True
            for entry, payload in zip(parsed_entries, payloads):
                entry_device_id = entry.get('device_id', device_id)
                token = get_bearer_token()
                status_code, response = send_to_erp(payload, API_ENDPOINT, token)
                print(f"➡️ Sent to ERP | Status: {status_code} | Response: {response}")
                log_test_result(device_id=entry_device_id, status=f"ERP Status: {status_code}", test_name=filename, remarks=str(response))
                if status_code != 200:
                    sent_all_payloads = False

            if sent_all_payloads:
                shutil.move(file_path, os.path.join(PROCESSED_DIR, filename))
                print(f"✅ File moved to processed: {filename}")
                log_test_result(device_id=device_id, status="Processed", test_name=filename, remarks="File moved to processed.")
            else:
                print(f"⚠️ Some payloads failed for file: {filename}")
                log_test_result(device_id=device_id, status="Partial Failure", test_name=filename, remarks="Some payloads failed.")
                all_success = False

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            log_test_result(device_id=device_id, status="Error", test_name=filename, remarks=str(e))
            all_success = False

    return all_success

if __name__ == "__main__":
    result = start_sdk()
    if result is True:
        print("🎉 All files processed successfully.")
        log_test_result(device_id="SDK", status="All Success", test_name="Batch", remarks="All files processed successfully.")
    elif result is False:
        print("⚠️ Some files had issues.")
        log_test_result(device_id="SDK", status="Batch Issues", test_name="Batch", remarks="Some files had issues.")
    else:
        print("📭 Nothing to process.")
        log_test_result(device_id="SDK", status="Nothing to Process", test_name="Batch", remarks="No files to process.")
