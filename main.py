from sensor import Sensor
from water_pump import WaterPump
from plant.plant import Plant
from database.plants_DAO import PlantsDAO
from time import sleep

# Inicializar o DAO
plants_dao = PlantsDAO()

# Criar um sensor de umidade analógico no pino ADC (pino 34) e uma bomba d'água no GPIO 17
sensor1 = Sensor(adc_pin=33)
water_pump1 = WaterPump(gpio_pin=27)

# Criar uma planta com o sensor e a bomba de água
plant1 = Plant(id=1, name="Planta1", sensor=sensor1, water_pump=water_pump1)

# Adicionar a planta ao banco de dados
#plants_dao.add_plant(plant1)

# Ler o valor de umidade do sensor da planta
plant = plants_dao.get_plant(1)

try:
    while True :
        if sensor1.read_percentage() > 20:
            water_pump1.turn_on()
            sleep(2)
            water_pump1.turn_off()
        sleep(1)
except  Exception as e:
    pass


