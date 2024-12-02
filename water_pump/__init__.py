from machine import ADC, Pin

class WaterPump:
    def __init__(self, gpio_pin: int):
        self.gpio_pin = gpio_pin
        self.pin = Pin(gpio_pin, Pin.OUT)
        self.is_running = False 

    def turn_on(self):
        if not self.is_running:
            self.pin.on()
            self.is_running = True 

    def turn_off(self):
        if self.is_running:
            self.pin.off()
            self.is_running = False 

    def to_dict(self):
        return {'gpio_pin': self.gpio_pin}