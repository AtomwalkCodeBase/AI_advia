# IOT SDK Configuration for Expense Claim API
API_URL = "https://crm.atomwalk.com/hr_api/add_claim/PMA_00001/"
AUTH_TOKEN = "d795ca107b331ca6136d00eb7d781ec5540224b3"
EMP_ID = "EMP-015"
PIN = "1234"

# Sensor Configuration
SENSOR_TYPE = 22  # DHT22
GPIO_PIN = 4      # Example GPIO pin

# API Configuration
CALL_MODE_SAVE = "CLAIM_SAVE"
CALL_MODE_UPDATE = "CLAIM_UPDATE"

# Default Values for Claims
DEFAULT_ITEM = "1"
DEFAULT_QUANTITY = "1"
DEFAULT_PROJECT_ID = None  # Can be set if needed

# File Configuration
SENSOR_DATA_FILENAME = "sensor_data.txt"
SENSOR_DATA_MIMETYPE = "text/plain"