import requests
import json
import io
from .config import API_URL, AUTH_TOKEN, EMP_ID, PIN

def send_to_erp(formatted_data, file_path=None, use_auth=True):
    """
    Send data to ERP with optional authentication
    Updated to match the expense claim API format exactly
    
    Args:
        formatted_data: Formatted data from formatter
        file_path: Optional file path
        use_auth: Whether to use authentication (default: True)
    """
    
    # Prepare headers - authentication is optional
    headers = {}
    if use_auth and AUTH_TOKEN:
        headers["Authorization"] = f"Token {AUTH_TOKEN}"
    else:
        print("⚠️ No authentication token provided - sending without authentication")
    
    # Extract data from formatted_data
    form_data = formatted_data.get('form_data', {})
    file_data = formatted_data.get('file_data', {})
    
    # Extract form fields
    remarks = form_data.get('remarks', 'No sensor data')
    item = form_data.get('item', '1')
    quantity = form_data.get('quantity', '1')
    expense_amt = form_data.get('expense_amt', '0')
    expense_date = form_data.get('expense_date', '25-04-2025')
    emp_id = form_data.get('emp_id', EMP_ID)
    call_mode = form_data.get('call_mode', 'CLAIM_SAVE')
    
    # Optional fields
    claim_id = form_data.get('claim_id')
    master_claim_id = form_data.get('m_claim_id')
    project_id = form_data.get('project_id')
    
    # Prepare multipart form data
    data = {
        "remarks": remarks,
        "item": item,
        "quantity": quantity,
        "expense_amt": expense_amt,
        "expense_date": expense_date,
        "emp_id": emp_id,
        "call_mode": call_mode,
    }
    
    # Add optional fields if present
    if claim_id:
        data["claim_id"] = claim_id
    if master_claim_id:
        data["m_claim_id"] = master_claim_id
    if project_id:
        data["project_id"] = project_id
    
    # Prepare file data
    files = {}
    if file_data and 'file_1' in file_data:
        file_info = file_data['file_1']
        file_content = file_info.get('uri', '')
        file_name = file_info.get('name', 'sensor_data.txt')
        file_type = file_info.get('type', 'text/plain')
        
        # Create file-like object from string content
        file_obj = io.BytesIO(file_content.encode('utf-8'))
        files['file_1'] = (file_name, file_obj, file_type)
    
    print("\n--- SENDING DATA TO EXPENSE CLAIM API ---")
    print("URL:", API_URL)
    print("Authentication:", "Token" if headers.get("Authorization") else "None")
    print("Call Mode:", call_mode)
    print("Form Data:", data)
    print("File Data:", "Present" if files else "None")
    
    try:
        response = requests.post(API_URL, headers=headers, data=data, files=files)
        print("Response Code:", response.status_code)
        print("Response:", response.text)
        
        if response.status_code == 200:
            print("✅ Claim submitted successfully!")
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"status": "success", "message": response.text}
        elif response.status_code == 401:
            print("❌ Authentication failed (401). Token might be invalid or expired.")
            print("You may need to update the AUTH_TOKEN in config.py with a fresh token.")
            return None
        else:
            print(f"❌ Data upload failed. Code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error sending data: {str(e)}")
        return None
