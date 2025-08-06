# data_formatter.py - Updated to match expense claim API format
from datetime import datetime
from .config import (
    CALL_MODE_SAVE, CALL_MODE_UPDATE, DEFAULT_ITEM, 
    DEFAULT_QUANTITY, DEFAULT_PROJECT_ID, SENSOR_DATA_FILENAME, SENSOR_DATA_MIMETYPE
)

def format_data(sensor_data, emp_id, is_edit_mode=False, claim_id=None, master_claim_id=None, project_id=None):
    """
    Format sensor data to match the expense claim API format
    
    Args:
        sensor_data: Dictionary containing sensor readings
        emp_id: Employee ID
        is_edit_mode: Whether this is an edit operation
        claim_id: Claim ID for updates
        master_claim_id: Master claim ID for additions
        project_id: Project ID (optional)
    """
    temperature = sensor_data.get('temperature', 0)
    humidity = sensor_data.get('humidity', 0)
    
    # Format date as "DD-MM-YYYY" (matching your API format)
    expense_date = datetime.now().strftime('%d-%m-%Y')
    
    # Create sensor data content for file upload
    sensor_content = f"Temperature: {temperature}°C, Humidity: {humidity}%"
    
    # Calculate expense amount based on sensor data (you can customize this logic)
    expense_amount = calculate_expense_amount(temperature, humidity)
    
    # Base form data matching your API format
    form_data = {
        "remarks": f"Sensor Reading - Temp: {temperature}°C, Humidity: {humidity}%",
        "item": DEFAULT_ITEM,
        "quantity": DEFAULT_QUANTITY,
        "expense_amt": str(expense_amount),
        "expense_date": expense_date,
        "emp_id": emp_id,
    }
    
    # Add call mode based on operation type
    if is_edit_mode:
        form_data["call_mode"] = CALL_MODE_UPDATE
        if claim_id:
            form_data["claim_id"] = claim_id
    else:
        form_data["call_mode"] = CALL_MODE_SAVE
        if master_claim_id:
            form_data["m_claim_id"] = master_claim_id
    
    if project_id:
        form_data["project_id"] = project_id
    
    
    file_data = {
        "file_1": {
            "uri": sensor_content, 
            "name": SENSOR_DATA_FILENAME,
            "type": SENSOR_DATA_MIMETYPE,
        }
    }
    
    return {
        "form_data": form_data,
        "file_data": file_data
    }

def calculate_expense_amount(temperature, humidity):
    """
    Calculate expense amount based on sensor readings
    You can customize this logic based on your business requirements
    """
    base_amount = 100
    
    temp_factor = max(0, (temperature - 20) * 2)  

    humidity_factor = 0
    if humidity < 30 or humidity > 70:
        humidity_factor = 50 
    
    total_amount = base_amount + temp_factor + humidity_factor
    
    return round(total_amount, 2)
