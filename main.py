import json
from obsact2py.generator import generate_program
from obsact2py.preprocessor import preprocess_indentation
from obsact2py.parser import parser

data = '''
dispositivo: {monitor}
dispositivo: {celular}
dispositivo: {tablet}
dispositivo: {Termometro, temperatura}
dispositivo: {Ventilador, potencia}

set temperatura = 39.
set potencia = 80.

enviar alerta ("Sistema iniciado") para todos: monitor, celular, tablet.

enviar alerta ("Temperatura em", temperatura) para todos: monitor, celular.

se temperatura > 30 entao
    enviar alerta ("Temperatura alta detectada", temperatura) para todos: monitor, celular, tablet.

se potencia > 70 && temperatura > 30 entao
    enviar alerta ("Potencia alta", potencia) para todos: monitor, celular.
    enviar alerta ("Verificar ventilador") para todos: monitor, tablet.
'''

preprocessed_code = preprocess_indentation(data)

print(preprocessed_code)

ast = parser.parse(preprocessed_code)
print("=== AST ===")
print(json.dumps(ast, indent=2, ensure_ascii=False))

print("\n=== Python Code ===")
python_code = generate_program(ast, arduino=False)
print(python_code)

with open("output.py", "w", encoding="utf-8") as f:
    f.write(python_code)
