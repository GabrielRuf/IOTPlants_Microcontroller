from machine import ADC, Pin

class Sensor:
    def __init__(self, adc_pin: int, calibration_min: int = 0, calibration_max: int = 4095):
        self.adc_pin = adc_pin
        self.adc = ADC(Pin(adc_pin))
        self.adc.width(ADC.WIDTH_12BIT)  # 12 bits = valores de 0 a 4095
        self.adc.atten(ADC.ATTN_11DB)    # Faixa de até 3.6V
        self.calibration_min = calibration_min  # Valor para 100% de umidade
        self.calibration_max = calibration_max  # Valor para 0% de umidade

    def read_value(self):
        """Lê o valor bruto do ADC."""
        return self.adc.read()

    def read_percentage(self):
        """Converte o valor lido do ADC em uma porcentagem invertida."""
        raw_value = self.read_value()
        # Limita o valor bruto dentro da faixa de calibração
        if raw_value < self.calibration_min:
            raw_value = self.calibration_min
        elif raw_value > self.calibration_max:
            raw_value = self.calibration_max
        # Calcula a porcentagem inversa
        percentage = 100 - ((raw_value - self.calibration_min) / 
                            (self.calibration_max - self.calibration_min)) * 100
        return percentage

    def to_dict(self):
        """Representa o sensor como um dicionário para salvar no banco de dados."""
        return {
            'adc_pin': self.adc_pin,
            'calibration_min': self.calibration_min,
            'calibration_max': self.calibration_max
        }
