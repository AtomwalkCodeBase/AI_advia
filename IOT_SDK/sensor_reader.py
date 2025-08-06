# sensor_reader.py
#import Adafruit_DHT
#from .config import SENSOR_TYPE, GPIO_PIN


#def read_sensor():
#    humidity, temperature = Adafruit_DHT.read_retry(SENSOR_TYPE, GPIO_PIN)
#   if humidity is not None and temperature is not None:
#       return {
#            "temperature": round(temperature, 2),
#            "humidity": round(humidity, 2)
#        }
#    else:
#       raise Exception("Sensor read failed")
def read_sensor():
    # Simulated test data
    return {
        "temperature": 26.5,
        "humidity": 58.3
    }

