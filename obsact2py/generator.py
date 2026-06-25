
def generate_program(ast, arduino):
    lines = []

    if arduino:
        lines.append("from obsact2py.runtime.inoaux import ligar, desligar, verificar, alerta")
        lines.append("import time")
    else:
        lines.append("from obsact2py.runtime.aux import ligar, desligar, verificar, alerta")
        lines.append("")

    lines.extend(generate_device_init(ast["devices"]))
    lines.append("")

    if arduino:
        lines.append("while True:")
        for cmd in ast["commands"]:
            lines.extend(generate_command(cmd, indent=1))
        lines.append(f"{tab(1)}time.sleep(0.1)")
    else:
        for cmd in ast["commands"]:
            lines.extend(generate_command(cmd, indent=0))

    return "\n".join(lines)

def generate_device_init(devices):
    lines = []
    initialized = set()

    for device in devices:
        obs = device.get("observation")

        if obs is not None and obs not in initialized:
            lines.append(f"{obs} = 0")      # Inicializacao com 0
            initialized.add(obs)

    return lines

def generate_command(cmd, indent=0):
    type = cmd["type"]

    if type == "assignment":
        return generate_assignment(cmd, indent)
    if type == "execute":
        return generate_execute(cmd, indent)
    if type == "alert":
        return generate_alert(cmd, indent)
    if type == "broadcast_alert":
        return generate_broadcast_alert(cmd, indent)
    if type == "conditional_if":
        return generate_if(cmd, indent)
    if type == "conditional_if_else":
        return generate_if_else(cmd, indent)
    
    raise ValueError(f"Tipo de comando desconhecido: {type}")

def tab(indent):
    return "    " * indent

def generate_value(value):
    if isinstance(value, bool):
        return "True" if value else "False"

    if isinstance(value, int):
        return str(value)

    if isinstance(value, str):
        return value

    if isinstance(value, dict):
        if value["type"] == "verify":
            return f'verificar("{value["target"]}")'

    raise ValueError(f"Valor inválido para geração: {value}")

def generate_assignment(cmd, indent=0):
    var_name = cmd["var"]
    value = generate_value(cmd["value"])

    return [f"{tab(indent)}{var_name} = {value}"]

def generate_execute(cmd, indent=0):
    action = cmd["action"]
    target = cmd["target"]

    return [f'{tab(indent)}{action}("{target}")']

def generate_alert(cmd, indent=0):
    target = cmd["target"]
    message = repr(cmd["message"])
    var_obs = cmd.get("var_obs")

    if var_obs is None:
        return [f'{tab(indent)}alerta("{target}", {message})']

    return [f'{tab(indent)}alerta("{target}", {message}, {var_obs})']

def generate_broadcast_alert(cmd, indent=0):
    lines = []
    for target in cmd["target"]:
        var_obs = cmd.get("var_obs")
        if var_obs is None:
            lines.append(f'{tab(indent)}alerta("{target}", {repr(cmd["message"])})')
        else:
            lines.append(f'{tab(indent)}alerta("{target}", {repr(cmd["message"])}, {var_obs})')
    return lines

# ===== Conditions =====

def generate_condition_side(side):
    if isinstance(side, str):
        return side

    if isinstance(side, dict):
        if side["type"] == "verify":
            return f'verificar("{side["target"]}")'

    raise ValueError(f"Lado inválido da condição: {side}")

def generate_condition(condition):
    left = generate_condition_side(condition["left"])
    op = condition["oplogic"]
    right = generate_value(condition["right"])

    current = f"{left} {op} {right}"

    if "and" in condition:
        return f"{current} and {generate_condition(condition['and'])}"

    return current

def generate_if(cmd, indent=0):
    lines = []

    condition = generate_condition(cmd["condition"])

    lines.append(f"{tab(indent)}if {condition}:")

    for inner_cmd in cmd["commands_0"]:
        lines.extend(generate_command(inner_cmd, indent + 1))

    return lines

def generate_if_else(cmd, indent=0):
    lines = []

    condition = generate_condition(cmd["condition"])

    lines.append(f"{tab(indent)}if {condition}:")

    for inner_cmd in cmd["commands_0"]:
        lines.extend(generate_command(inner_cmd, indent + 1))

    lines.append(f"{tab(indent)}else:")

    for inner_cmd in cmd["commands_1"]:
        lines.extend(generate_command(inner_cmd, indent + 1))

    return lines

