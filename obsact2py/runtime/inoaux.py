import serial
import time

arduino = serial.Serial('/dev/cu.usbserial-2120', 9600, timeout=1)
time.sleep(2)
arduino.reset_input_buffer()

_device_states = {}

def send_command(command):
    arduino.reset_input_buffer()
    arduino.write((command + "\n").encode())
    arduino.flush()
    time.sleep(0.05)

    response = arduino.readline().decode(errors="ignore").strip()
    return response


def ligar(namedevice):
    if namedevice == "led":
        response = send_command("ON:led")

        if response == "OK":
            _device_states[namedevice] = 1
            print("led ligado!")
            return 1

        print("Erro ao ligar led.")
        return -1

    print(f"Dispositivo '{namedevice}' não mapeado.")
    return -1


def desligar(namedevice):
    if namedevice == "led":
        response = send_command("OFF:led")

        if response == "OK":
            _device_states[namedevice] = 0
            print("led desligado!")
            return 0

        print("Erro ao desligar led.")
        return -1

    print(f"Dispositivo '{namedevice}' não mapeado.")
    return -1


def verificar(namedevice):
    if namedevice == "botao":
        response = send_command("READ:botao")

        if response == "1":
            print(namedevice + " esta ligado.")
            return 1

        if response == "0":
            print(namedevice + " esta desligado.")
            return 0

        print(f"Resposta inesperada do Arduino: {response}")
        return -1


def alerta(namedevice, msg, var=None):
    print(namedevice + " recebeu o alerta:")

    if var is not None:
        print(str(msg) + " " + str(var))
    else:
        print(str(msg))