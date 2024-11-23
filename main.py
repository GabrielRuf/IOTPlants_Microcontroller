from bluetooth_le import ESP32_BLE
from time import sleep
import network_config

def main():
    try:
        while True:
            esp = ESP32_BLE("IOTPlants")
            sleep(1000) 
    except  KeyboardInterrupt as e :
        print("Stopping process")

def database_test():
    from sensor import Sensor
    from water_pump import WaterPump
    from plant.plant import Plant
    from database.plants_DAO import PlantsDAO

    # Inicializar o DAO
    plants_dao = PlantsDAO()

    # Criar um sensor de umidade analógico no pino ADC (pino 34) e uma bomba d'água no GPIO 17
    sensor1 = Sensor(adc_pin=34)
    water_pump1 = WaterPump(gpio_pin=17)

    # Criar uma planta com o sensor e a bomba de água
    plant1 = Plant(id=1, name="Planta1", sensor=sensor1, water_pump=water_pump1)

    # Adicionar a planta ao banco de dados
    plants_dao.add_plant(plant1)

    # Ler o valor de umidade do sensor da planta
    plant = plants_dao.get_plant(1)

    print(plant.to_dict())


if __name__ == "__main__":
    database_test()
