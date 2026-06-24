import json
from generator import generate_program
from preprocessor import preprocess_indentation
from parser import parser

data = '''
dispositivo: {Termometro, temperatura}
dispositivo: {Celular}
dispositivo: {Monitor}
dispositivo: {Tablet}
dispositivo: {Ventilador, potencia}

set temperatura = 37.
set potencia = 10.

enviar alerta ("Sistema iniciado") para todos: Celular, Monitor, Tablet.

se temperatura > 30 entao
    enviar alerta ("Temperatura em", temperatura) Celular.
    enviar alerta ("Temperatura alta detectada", temperatura) para todos: Celular, Monitor, Tablet.

    se potencia < 20 && temperatura > 30 entao
        set potencia = 80.
        enviar alerta ("Potencia em", potencia) Celular.
        enviar alerta ("Ventilador ajustado para", potencia) para todos: Celular, Monitor.

        se potencia > 70 entao
            set potencia = 100.
            enviar alerta ("Potencia maxima atingida", potencia) para todos: Celular, Monitor, Tablet.

    se potencia > 70 entao
        set potencia = 100.
        enviar alerta ("Potencia final em", potencia) para todos: Celular, Monitor.

se potencia < 20 && temperatura > 30 entao
    set potencia = 80.
    enviar alerta ("Potencia atualizada", potencia) para todos: Celular, Tablet.
'''

preprocessed_code = preprocess_indentation(data)

print(preprocessed_code)

ast = parser.parse(preprocessed_code)
print("=== AST ===")
print(json.dumps(ast, indent=2, ensure_ascii=False))

print("\n=== Python Code ===")
python_code = generate_program(ast)
print(python_code)

with open("output.py", "w", encoding="utf-8") as f:
    f.write(python_code)
