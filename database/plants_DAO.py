from tinydb import TinyDB, Query
from sensor import Sensor
from water_pump import WaterPump
from plant.plant import Plant

class PlantsDAO:
    def __init__(self, db_path='plants_db.json'):
        self.db = TinyDB(db_path)
        self.plants_table = self.db.table('plants')

    def add_plant(self, plant: Plant):
        if self.plant_exists(plant.id):
            raise ValueError(f'Plant with ID {plant.id} already exists.')
        self.plants_table.insert(plant.to_dict())
        print(f'Plant "{plant.name}" added successfully!')

    def get_plant(self, plant_id: int):
        PlantQuery = Query()
        result = self.plants_table.get(PlantQuery.id == plant_id)
        if result:
            sensor = Sensor(result['sensor']['adc_pin'])
            water_pump = None
            if 'water_pump' in result:
                water_pump = WaterPump(result['water_pump']['gpio_pin'])
            return Plant(result['id'], result['name'], sensor, water_pump)
        return None

    def update_plant(self, plant_id: int, name: str = None, sensor: Sensor = None, water_pump: WaterPump = None):
        PlantQuery = Query()
        update_data = {}
        if name:
            update_data['name'] = name
        if sensor:
            update_data['sensor'] = sensor.to_dict()
        if water_pump:
            update_data['water_pump'] = water_pump.to_dict()
        self.plants_table.update(update_data, PlantQuery.id == plant_id)
        print(f'Plant ID {plant_id} updated successfully!')

    def delete_plant(self, plant_id: int):
        PlantQuery = Query()
        self.plants_table.remove(PlantQuery.id == plant_id)
        print(f'Plant ID {plant_id} deleted successfully!')

    def plant_exists(self, plant_id: int):
        PlantQuery = Query()
        return self.plants_table.contains(PlantQuery.id == plant_id)

    def list_plants(self):
        all_plants = self.plants_table.all()
        plants_list = []
        for plant in all_plants:
            sensor = Sensor(plant['sensor']['adc_pin'])
            water_pump = None
            if 'water_pump' in plant:
                water_pump = WaterPump(plant['water_pump']['gpio_pin'])
            plants_list.append(Plant(plant['id'], plant['name'], sensor, water_pump))
        return plants_list