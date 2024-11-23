from micropython import const

class Events:
    def __init__(self):
        self._IRQ_CENTRAL_CONNECT = const(1)
        self._IRQ_CENTRAL_DISCONNECT = const(2)
        self._IRQ_GATTS_WRITE = const(3)
        self._IRQ_GATTS_READ_REQUEST = const(4)
        self._IRQ_SCAN_RESULT = const(5)
        self._IRQ_SCAN_DONE = const(6)
        self._IRQ_PERIPHERAL_CONNECT = const(7)
        self._IRQ_PERIPHERAL_DISCONNECT = const(8)
        self._IRQ_GATTC_SERVICE_RESULT = const(9)
        self._IRQ_GATTC_SERVICE_DONE = const(10)
        self._IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
        self._IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
        self._IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
        self._IRQ_GATTC_DESCRIPTOR_DONE = const(14)
        self._IRQ_GATTC_READ_RESULT = const(15)
        self._IRQ_GATTC_READ_DONE = const(16)
        self._IRQ_GATTC_WRITE_DONE = const(17)
        self._IRQ_GATTC_NOTIFY = const(18)
        self._IRQ_GATTC_INDICATE = const(19)
        self._IRQ_GATTS_INDICATE_DONE = const(20)
        self._IRQ_MTU_EXCHANGED = const(21)
        self._IRQ_L2CAP_ACCEPT = const(22)
        self._IRQ_L2CAP_CONNECT = const(23)
        self._IRQ_L2CAP_DISCONNECT = const(24)
        self._IRQ_L2CAP_RECV = const(25)
        self._IRQ_L2CAP_SEND_READY = const(26)
        self._IRQ_CONNECTION_UPDATE = const(27)
        self._IRQ_ENCRYPTION_UPDATE = const(28)
        self._IRQ_GET_SECRET = const(29)
        self._IRQ_SET_SECRET = const(30)

    # Método para obter o nome do evento
    def get_event_name(self, value):
        for name, event in self.__dict__.items():
            if event == value:
                return name
        return None


