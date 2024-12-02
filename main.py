from bluetooth_le import ESP32_BLE
from database.plants_DAO import PlantsDAO
from time import sleep

plants_dao = PlantsDAO()

plants = plants_dao.list_plants()
device = ESP32_BLE("IOTPlants",plants,plants_dao)
try:
    while True :
        sleep(1)
except  Exception as e:
    print(e)


