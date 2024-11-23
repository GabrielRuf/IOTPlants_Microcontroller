import ustruct
from machine import Timer, Pin
import ubluetooth
from bluetooth_le.events import Events
from bluetooth_le.advertising_payload import advertising_payload
from time import sleep

class ESP32_BLE:
    SERVICE_UUID = ubluetooth.UUID("0000183F-0000-1000-8000-00805f9b34fb")
    NOTIFY_CHAR_UUID = ubluetooth.UUID("00002FFF-0000-1000-8000-00805f9b34fb")
    WRITE_CHAR_UUID = ubluetooth.UUID("00002AFF-0000-1000-8000-00805f9b34fb")

    def __init__(self, name, manufacturer_data=None):
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

    def ble_irq(self, event, data):
        if event == self.events._IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)

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
        pass

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
            print("Iniciando leitura de peso...")

    def stop_weight_reading(self):
        if self.timer:
            self.timer.deinit()
            self.timer = None
            print("Parando leitura de peso...")

    def read_umity(self, t):
        pass


