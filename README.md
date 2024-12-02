# ESP32 BLE Plant Monitor

Este projeto utiliza o ESP32 para monitorar e controlar plantas via Bluetooth Low Energy (BLE). Ele permite cadastrar, atualizar, remover e listar plantas, além de monitorar a umidade do solo e controlar uma bomba de água para irrigação automática.

## Funcionalidades

- **Cadastro de plantas**: Adiciona novas plantas ao sistema, incluindo sensor de umidade e bomba de água.
- **Remoção de plantas**: Remove plantas cadastradas no sistema.
- **Atualização de plantas**: Atualiza as informações de plantas cadastradas.
- **Listagem de plantas**: Lista todas as plantas cadastradas.
- **Monitoramento da umidade**: Lê periodicamente a umidade do solo de cada planta cadastrada.
- **Irrigação automática**: Liga ou desliga a bomba de água com base na umidade do solo.

## Instalação

1. Clone este repositório no seu ambiente de desenvolvimento.
2. Carregue o código no seu ESP32 usando um ambiente de desenvolvimento como o [Thonny](https://thonny.org/) ou o [esptool.py](https://github.com/espressif/esptool).
3. Certifique-se de ter todas as dependências instaladas e o hardware necessário conectado corretamente (sensores e bombas de água).

## Comandos BLE

A comunicação com o ESP32 é feita via BLE, enviando comandos específicos ao dispositivo. Cada comando pode ser enviado como uma string de texto. A seguir estão os comandos disponíveis:

### Comando `add`
Adiciona uma nova planta ao sistema. O formato do comando é:

```
add:<plant_id>:<plant_name>:<gpio_sensor>:<gpio_water_pump>
```

- `plant_id`: Identificador único da planta.
- `plant_name`: Nome da planta.
- `gpio_sensor`: GPIO ao qual o sensor de umidade está conectado.
- `gpio_water_pump`: GPIO ao qual a bomba de água está conectada.

**Exemplo:**

```
add:1:Cacto:34:25
```

Resultado: Cadastra uma nova planta chamada "Cacto" com o sensor de umidade no GPIO 34 e a bomba de água no GPIO 25.

### Comando `remove`
Remove uma planta cadastrada no sistema. O formato do comando é:

```
remove:<plant_id>
```

- `plant_id`: Identificador único da planta.

**Exemplo:**

```
remove:1
```

Resultado: Remove a planta com `plant_id` igual a 1 do sistema.

### Comando `update`
Atualiza as informações de uma planta já cadastrada. O formato do comando é:

```
update:<plant_id>:<plant_name>:<gpio_sensor>:<gpio_water_pump>
```

- `plant_id`: Identificador da planta a ser atualizada.
- `plant_name`: Novo nome da planta.
- `gpio_sensor`: Novo GPIO do sensor de umidade.
- `gpio_water_pump`: Novo GPIO da bomba de água.

**Exemplo:**

```
update:1:Rosa:35:26
```

Resultado: Atualiza a planta com `plant_id` 1 para o nome "Rosa", com o sensor de umidade no GPIO 35 e a bomba de água no GPIO 26.

### Comando `list`
Lista todas as plantas cadastradas no sistema. O formato do comando é:

```
list:
```

Este comando não exige parâmetros adicionais.

Resultado: Retorna uma lista de todas as plantas cadastradas, com seus detalhes (ID, nome, GPIOs dos sensores e bombas).

## Exemplo de Uso

Ao enviar um comando `add` para o ESP32 via BLE:

```
add:1:Cacto:34:25
```

O ESP32:

- Cadastrará a planta "Cacto".
- Configurará o sensor de umidade no GPIO 34.
- Configurará a bomba de água no GPIO 25.

A planta será monitorada periodicamente. Se a umidade do solo cair abaixo de 20%, a bomba de água será ativada automaticamente para irrigar a planta.

## Estrutura do Código

### Classe `ESP32_BLE`

A classe `ESP32_BLE` é responsável pela comunicação BLE e pela interação com as plantas e seus sensores. Ela define um serviço BLE com dois UUIDs:

- `SERVICE_UUID`: UUID do serviço BLE.
- `NOTIFY_CHAR_UUID`: UUID para enviar notificações ao cliente.
- `WRITE_CHAR_UUID`: UUID para receber comandos do cliente.

#### Principais métodos:

- `__init__(self, name, plants, dao, manufacturer_data=None)`: Inicializa o dispositivo BLE, registrando os serviços e características, e começa a anunciar o dispositivo.
- `ble_irq(self, event, data)`: Gerencia os eventos BLE, como conexões e recebimento de dados.
- `register(self)`: Registra o serviço BLE com características de notificação e escrita.
- `handle_write_event(self, data)`: Lida com os comandos recebidos via BLE.
- `send(self, data)`: Envia notificações para dispositivos conectados.
- `_advertise(self)`: Inicia o processo de anúncio BLE.
- `start_umity_reading(self)`: Inicia a leitura periódica de umidade.
- `stop_umity_reading(self)`: Para a leitura periódica de umidade.
- `read_umity(self, t)`: Faz a leitura da umidade e controla a bomba de água.

## Licença

Consulte o arquivo [LICENSE](LICENSE) para obter mais detalhes.
