import network
import utime
import _thread
from machine import Pin, reset

class Wifi():
    def __init__(self, rede="NET_2G5186E2", senha="4F5186E2"):
        self.rede = rede
        self.senha = senha
        self.sta_if = network.WLAN(network.STA_IF)

        # Faz o scan das redes Wi-Fi disponíveis
        self.scan_networks()

        # Inicia o processo de conexão
        self.connect()
        
        # Inicia a thread para monitorar a conexão
        _thread.start_new_thread(self.monitor_connection, ())

    def scan_networks(self):
        try:
            # Ativa a interface Wi-Fi (caso ainda não esteja ativa)
            if not self.sta_if.active():
                self.sta_if.active(True)
            
            print("Scanning for available networks...")
            redes = self.sta_if.scan()  # Realiza o scan das redes Wi-Fi
            
            # Printar as redes encontradas
            for rede in redes:
                ssid = rede[0].decode('utf-8')  # Nome da rede (SSID)
                rssi = rede[3]  # Intensidade do sinal (RSSI)
                print(f"SSID: {ssid}, Signal strength: {rssi} dBm")
        except Exception as e:
            print("Failed to scan networks:", e)

    def connect(self):
        try:
            if not self.sta_if.isconnected():
                print(f'Connecting to network {self.rede}...')
                self.sta_if.active(True)
                self.sta_if.connect(self.rede, self.senha)
                while not self.sta_if.isconnected():
                    utime.sleep(1)
            print('Network config:', self.sta_if.ifconfig())
        except Exception as e:
            print(e)
            reset()            

    def monitor_connection(self):
        while True:
            if not self.sta_if.isconnected():
                print('Connection lost. Reconnecting...')
                self.connect()
            utime.sleep(1)

# Instancia o objeto Wifi e inicia o processo
Wifi()
