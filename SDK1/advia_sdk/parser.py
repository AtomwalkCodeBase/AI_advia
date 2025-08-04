import re

# Control characters for ASTM E1381
STX = '\x02'
ETX = '\x03'
EOT = '\x04'
ENQ = '\x05'
ACK = '\x06'
NAK = '\x15'
CR = '\x0D'
LF = '\x0A'

def strip_control_chars(raw_data):
    """
    Remove ASTM E1381 framing and extract pure E1394 message block.
    """
    # Extract text between STX and ETX (ASTM frame)
    pattern = re.compile(rf"{STX}(.*?){ETX}.*?", re.DOTALL)
    match = pattern.search(raw_data)

    if match:
        clean_data = match.group(1)
        # Split lines on carriage return
        return clean_data.strip().split(CR)
    else:
        # If no framing detected, assume it's plain E1394 lines
        return raw_data.strip().splitlines()

def parse_astm(raw_data):
    """
    Parse raw ASTM data (E1381 or E1394) and return a list of test results.
    """
    results = []
    rat_no = None
    device_id = None
    lines = strip_control_chars(raw_data)

    for line in lines:
        parts = line.split('|')

        if line.startswith('H|'):
            device_id = parts[4]
        elif line.startswith('P|'):
            rat_no = parts[3]  # Usually where animal/patient ID is stored

        elif line.startswith('R|'):
            test_name = parts[2].split('^')[-1]
            test_value = parts[3]
            results.append({
                'rat_no': rat_no,
                'test_name': test_name,
                'test_value': test_value,
                'device_id' : device_id
                  })

    return results
