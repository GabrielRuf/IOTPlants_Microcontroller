import ustruct
from machine import Timer, Pin
import ubluetooth
from bluetooth_le.events import Events
from bluetooth_le.advertising_payload import advertising_payload
from time import sleep
from plant.plant import Plant, Sensor, WaterPump

class ESP32_BLE:
    SERVICE_UUID = ubluetooth.UUID("0000183F-0000-1000-8000-00805f9b34fb")
    NOTIFY_CHAR_UUID = ubluetooth.UUID("00002FFF-0000-1000-8000-00805f9b34fb")
    WRITE_CHAR_UUID = ubluetooth.UUID("00002AFF-0000-1000-8000-00805f9b34fb")

    def __init__(self, name, plants,dao ,manufacturer_data=None):
        self.name = name
        self.led = Pin(2, Pin.OUT) 
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.ble_irq)
        self._connections = set()
        self.events = Events()
        self.timer = None
        self.manufacturer_data = manufacturer_data or bytearray([0x12, 0x23])
        self.register()
        self._advertise()
        self.plants = plants
        self.plants_dao = dao

    def ble_irq(self, event, data):
        if event == self.events._IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            self.start_umity_reading()

        elif event == self.events._IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            self._advertise()
            
        elif event == self.events._IRQ_GATTS_WRITE:
            self.handle_write_event(data)

    def register(self):
        notify_char = (
            self.NOTIFY_CHAR_UUID,
            ubluetooth.FLAG_READ | ubluetooth.FLAG_NOTIFY,
        )

        write_char = (
            self.WRITE_CHAR_UUID,
            ubluetooth.FLAG_WRITE,
        )

        service = (
            self.SERVICE_UUID,
            (notify_char, write_char),
        )

        ((self.notifychar, self.writechar),) = self.ble.gatts_register_services([service])

    def handle_write_event(self, data):
        try:
            conn_handle, value_handle = data
            if value_handle == self.writechar:
                payload = self.ble.gatts_read(value_handle).decode('utf-8')
                if payload.startswith("add:"):
                    _ ,plant_id, plant_name, gpio_sensor, gpio_water_pump = payload.split(":")
                    sensor = Sensor(int(gpio_sensor))
                    water_pump = WaterPump(int(gpio_water_pump))
                    plant = Plant(plant_id,plant_name,sensor,water_pump)
                    self.plants_dao.add_plant(plant)
                    self.send("Plata cadastrada!")
                    
                elif payload.startswith("remove:"):
                    _ , plant_id = payload.split(":")
                    self.plants_dao.delete_plant(plant_id)
                elif payload.startswith("update:"):
                    
                    _ ,plant_id ,plant_name, gpio_sensor, gpio_water_pump = payload.split(":")
                    sensor = Sensor(gpio_sensor)
                    water_pump = WaterPump(gpio_water_pump)
                    self.plants_dao.update_plant(plant_id,plant_name, sensor,water_pump)
                    
                elif payload.startswith("list:"):
                    plants = self.plants_dao.list_plants()
                    self.send(plants)
        except Exception as e :
            print(e)
                
    def send(self, data):
        for conn_handle in self._connections:
            self.ble.gatts_notify(conn_handle, self.notifychar, data)

    def _advertise(self):
        # Constrói o payload de publicidade com os dados do fabricante
        adv_data = advertising_payload(
            name=self.name,           # Nome do dispositivo
            manufacturer_data=self.manufacturer_data
        )

        # Inicia a publicidade
        self.ble.gap_advertise(100000, adv_data)
        print(f"Anunciando: {self.name}")

    def start_umity_reading(self):
        if self.timer is None and len(self._connections) > 0:
            self.timer = Timer(-1)
            self.timer.init(period=10000, mode=Timer.PERIODIC, callback=self.read_umity)
            print("Iniciando leitura da humidade...")

    def stop_umity_reading(self):
        if self.timer:
            self.timer.deinit()
            self.timer = None
            print("Parando leitura de peso...")

    def read_umity(self, t):
        for plant in self.plants:
            water_percent = plant.sensor.read_percentage()
            print(water_percent)
            if water_percent < 20:
                plant.water_pump.turn_on()
            else:
                plant.water_pump.turn_off()

