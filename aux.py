_device_states = {}

def ligar(namedevice):
    _device_states[namedevice] = 1
    print(namedevice + " ligado!")
    return 1

def desligar(namedevice):
    _device_states[namedevice] = 0
    print(namedevice + " desligado!")
    return 0

def verificar(namedevice):
    state = _device_states[namedevice]
    if state == 1:
        print(namedevice + " est ligado .")
        return 1
    elif state == 0:
        print(namedevice + " est desligado.")
        return 0
    else:
        print(f"Error: Estado retornado diferente do esperado ({state}).")
        return -1

def alerta(namedevice, msg, var=None):
    print(namedevice + " recebeu o alerta:\n")
    if var is not None:
        print(msg + " " + var)
    else:
        print(msg)