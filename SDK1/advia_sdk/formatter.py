from datetime import datetime

# 🧠 Mapping test names from ADVIA to ERP-expected names
TEST_NAME_MAPPING = {
    "RBC": "Measuring weight",
    "WBC": "White Cell Count",
    "HGB": "Hemoglobin Level"
}

def format_for_erp(entry):
    now = datetime.now()
    mapped_test_name = TEST_NAME_MAPPING.get(entry['test_name'], entry['test_name'])

    return {
        "test_data": {
            "test_type_id": 1,
            "call_mode": "ADD_TEST",
            "group_id": 1,
            "test_name": mapped_test_name,
            "rat_no": entry['rat_no'],
            "test_time": now.strftime("%I:%M %p"),
            "test_date": now.strftime("%d-%m-%Y"),
            "test_value": entry['test_value'],
            "remarks": " "
        }
    }
