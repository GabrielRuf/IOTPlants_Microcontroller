from machine import ADC, Pin

class WaterPump:
    def __init__(self, gpio_pin: int):
        self.gpio_pin = gpio_pin
        self.pin = Pin(gpio_pin, Pin.OUT) 

    def turn_on(self):
        self.pin.on()

    def turn_off(self):
        self.pin.off()

    def to_dict(self):
        return {'gpio_pin': self.gpio_pin}