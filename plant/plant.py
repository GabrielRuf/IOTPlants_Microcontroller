from sensor import Sensor
from water_pump import WaterPump

class Plant:
    def __init__(self, id: int, name: str, sensor: Sensor, water_pump: WaterPump = None):
        self.id = id
        self.name = name
        self.sensor = sensor
        self.water_pump = water_pump

    def to_dict(self):
        plant_dict = {
            'id': self.id,
            'name': self.name,
            'sensor': self.sensor.to_dict()
        }
        if self.water_pump:
            plant_dict['water_pump'] = self.water_pump.to_dict()
        return plant_dict