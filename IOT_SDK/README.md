# IOT SDK - Expense Claim API Integration

## 📋 Overview

The IOT SDK has been updated to integrate with your expense claim API format. It reads sensor data (temperature, humidity) and submits it as expense claims using the exact same format as your React Native application.

## 🔧 API Format Compatibility

The IOT SDK now sends data in the exact format your API expects:

```javascript
// Your React Native format
const formData = new FormData();
formData.append('file_1', {
  uri: fileUri,
  name: fileName,
  type: fileMimeType,
});
formData.append('remarks', remark);
formData.append('item', item);
formData.append('quantity', '1');
formData.append('expense_amt', claimAmount);
formData.append('expense_date', formattedDate);
formData.append('emp_id', empId);
formData.append('call_mode', 'CLAIM_SAVE'); // or 'CLAIM_UPDATE'
```

## 📁 File Structure

```
IOT_SDK/
├── config.py          # Configuration settings
├── sensor_reader.py   # Sensor data reading
├── formatter.py       # Data formatting for API
├── sender.py          # API communication
├── main.py           # Main SDK functions
├── example_usage.py  # Usage examples
└── README.md         # This file
```

## ⚙️ Configuration

Edit `config.py` to set your API credentials and settings:

```python
# API Configuration
API_URL = "https://crm.atomwalk.com/hr_api/add_claim/PMA_00001/"

# Authentication Configuration
# Set AUTH_TOKEN to None if your API doesn't require authentication
AUTH_TOKEN = None  # Set to your token if needed
USE_AUTHENTICATION = False  # Set to True if API requires authentication

EMP_ID = "EMP-015"

# Sensor Configuration
SENSOR_TYPE = 22  # DHT22
GPIO_PIN = 4      # GPIO pin for sensor

# API Modes
CALL_MODE_SAVE = "CLAIM_SAVE"
CALL_MODE_UPDATE = "CLAIM_UPDATE"
```

## 🚀 Usage Examples

### Basic Usage

```python
from IOT_SDK.main import submit_new_claim

# Submit a new expense claim with sensor data
success = submit_new_claim()
```

### With Project ID

```python
from IOT_SDK.main import submit_new_claim

# Submit claim with project ID
success = submit_new_claim(project_id="PROJ-001")
```

### With Master Claim ID

```python
from IOT_SDK.main import submit_new_claim

# Submit claim with master claim ID
success = submit_new_claim(master_claim_id="MCLAIM-2024-001")
```

### Update Existing Claim

```python
from IOT_SDK.main import update_existing_claim

# Update an existing claim
success = update_existing_claim(claim_id="CLAIM-2024-001")
```

### Advanced Usage

```python
from IOT_SDK.main import start_sdk

# Use all parameters (no authentication)
success = start_sdk(
    is_edit_mode=False,
    master_claim_id="MCLAIM-2024-002",
    project_id="PROJ-002",
    use_auth=False
)
```

### Authentication Options

```python
from IOT_SDK.main import submit_new_claim

# Without authentication (default)
success = submit_new_claim(use_auth=False)

# With authentication (if you have a token)
success = submit_new_claim(use_auth=True)
```

## 📊 Data Flow

1. **Sensor Reading**: Reads temperature and humidity from DHT22 sensor
2. **Data Formatting**: Formats sensor data to match your API format
3. **Expense Calculation**: Calculates expense amount based on sensor readings
4. **API Submission**: Sends multipart/form-data to your expense claim API
5. **Response Handling**: Processes API response and returns success/failure

## 💰 Expense Calculation Logic

The SDK calculates expense amounts based on sensor readings:

```python
def calculate_expense_amount(temperature, humidity):
    base_amount = 100
    
    # Temperature factor: $2 per degree above 20°C
    temp_factor = max(0, (temperature - 20) * 2)
    
    # Humidity factor: $50 for extreme humidity (<30% or >70%)
    humidity_factor = 0
    if humidity < 30 or humidity > 70:
        humidity_factor = 50
    
    return base_amount + temp_factor + humidity_factor
```

## 📤 API Request Format

The SDK sends requests in this exact format:

```python
# Form Data
{
    "remarks": "Sensor Reading - Temp: 25.5°C, Humidity: 60%",
    "item": "1",
    "quantity": "1",
    "expense_amt": "111.0",
    "expense_date": "25-04-2025",
    "emp_id": "EMP-015",
    "call_mode": "CLAIM_SAVE",
    "project_id": "PROJ-001",  # Optional
    "m_claim_id": "MCLAIM-2024-001",  # Optional
    "claim_id": "CLAIM-2024-001"  # For updates
}

# File Data
{
    "file_1": {
        "uri": "Temperature: 25.5°C, Humidity: 60%",
        "name": "sensor_data.txt",
        "type": "text/plain"
    }
}
```

## 🔄 Continuous Monitoring

For continuous monitoring, use the example script:

```bash
python IOT_SDK/example_usage.py
```

This will:
- Run basic examples
- Offer continuous monitoring option
- Submit claims every 30 seconds
- Show real-time status

## 🛠️ Installation

1. Install required packages:
```bash
pip install requests
```

2. For Raspberry Pi with DHT22 sensor:
```bash
pip install Adafruit_DHT
```

3. Configure your settings in `config.py`

4. Test the SDK:
```bash
python IOT_SDK/main.py
```

## 📝 Logging

The SDK provides detailed logging:

```
🔍 Reading sensor data...
📝 Formatting data for expense claim API...
📤 Sending data to expense claim API...
--- SENDING DATA TO EXPENSE CLAIM API ---
URL: https://crm.atomwalk.com/hr_api/add_claim/PMA_00001/
Call Mode: CLAIM_SAVE
Form Data: {...}
File Data: Present
Response Code: 200
✅ Claim submitted successfully!
```

## 🔧 Customization

### Modify Expense Calculation

Edit the `calculate_expense_amount()` function in `formatter.py` to implement your business logic.

### Add More Sensors

Extend `sensor_reader.py` to read additional sensors and update the formatter accordingly.

### Custom API Endpoints

Modify `config.py` to use different API endpoints for different environments.

## 🚨 Error Handling

The SDK handles various error scenarios:

- **401 Unauthorized**: Invalid or expired token
- **Network Errors**: Connection issues
- **Sensor Errors**: Hardware problems
- **API Errors**: Server-side issues

## 📞 Support

For issues or questions:
1. Check the logs for detailed error messages
2. Verify your API credentials in `config.py`
3. Test sensor connectivity
4. Review the example usage scripts

## 🔄 Version History

- **v2.0**: Updated to match expense claim API format
- **v1.0**: Basic sensor data submission

---

**Note**: This SDK is designed to work with your existing expense claim API without any modifications to your backend system. 