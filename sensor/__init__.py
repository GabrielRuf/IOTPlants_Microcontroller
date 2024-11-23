from machine import ADC, Pin

class Sensor:
    def __init__(self, adc_pin: int):
        self.adc_pin = adc_pin
        self.adc = ADC(Pin(adc_pin))

    def read_value(self):
        return self.adc.read()

    def to_dict(self):
        return {'adc_pin': self.adc_pin}