import ply.lex as lex

reserved = {
    'dispositivo': 'DISPOSITIVO',
    'set': 'SET',
    'se': 'SE',
    'entao': 'ENTAO',
    'senao': 'SENAO',
    'enviar': 'ENVIAR',
    'alerta': 'ALERTA',
    'ligar': 'LIGAR',
    'desligar': 'DESLIGAR',
    'verificar': 'VERIFICAR',
    'para': 'PARA',
    'todos': 'TODOS',

    'True': 'BOOL',
    'False': 'BOOL',
    'TRUE': 'BOOL',
    'FALSE': 'BOOL'
}

tokens = [
    'NUM',          # int > 0
    'ID',           # namedevice / observation
    'STRING',       # msg

    # Symbols
    'LBRACE',       # {
    'RBRACE',       # }
    'LPAREN',       # (
    'RPAREN',       # )
    'COMMA',        # ,
    'DOT',          # .
    'COLON',        # :

    # Logical operators
    'ASSIGN',       # =
    'EQ',           # ==
    'NEQ',          # !=
    'GT',           # >
    'GE',           # >=
    'LT',           # <
    'LE',           # <=
    'AND',          # &&
] + list(set(reserved.values()))

# -- Some Regex -- 

t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA   = r','
t_DOT     = r'\.'
t_COLON   = r':'

t_EQ      = r'=='
t_NEQ     = r'!='
t_GE      = r'>='
t_LE      = r'<='
t_GT      = r'>'
t_LT      = r'<'
t_ASSIGN  = r'='
t_AND     = r'&&'

t_ignore  = ' \t'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)    # t > 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, "ID")

    if t.type == 'BOOL':
        t.value = t.value.lower() == 'true'

    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]   # "" removal
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Caractere ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == '__main__':
    tests = {
        "Teste 1: Atribuição e Condicional Simples": '''
            dispositivo: {Termometro, temperatura}
            dispositivo: {ventilador, potencia}
            set temperatura = 40.
            set potencia = 90.
            se temperatura > 30 entao ligar ventilador.
        ''',

        "Teste 2: Condicional Aninhado e Função Verificar": '''
            dispositivo: {Termometro, temperatura}
            dispositivo: {ventilador, potencia}
            set temperatura = 40.
            se temperatura > 30 entao
                set estado_ventilador = verificar(ventilador).
                se estado_ventilador == 0 entao ligar ventilador.
                set potencia = 90.
        ''',

        "Teste 3: Operador Lógico, Broadcast e Concatenação": '''
            dispositivo: {monitor}
            dispositivo: {celular}
            dispositivo: {Termometro, temperatura}
            se temperatura > 30 && movimento == True entao
                enviar alerta ("Temperatura em", temperatura) para todos:
                monitor, celular
        ''',

        "Teste 4: Condicional com Senao": '''
            dispositivo: {lampada, potencia}
            dispositivo: {sensor_presenca, movimento}
            se movimento == True entao
                ligar lampada.
            senao
                desligar lampada.
        ''',

        "Teste 5: Cobertura de Arestas (Operadores, False e Alerta Simples)": '''
            dispositivo: {umidificador, umidade}
            dispositivo: {janela}
            dispositivo: {celular}
            
            set umidade = 40.
            
            se umidade <= 30 && movimento != False entao
                ligar umidificador.
                enviar alerta ("Nivel critico atingido") celular.
                set estado_janela = verificar(janela).
        ''',

        "Teste 6: Booleanos": '''
            dispositivo: {lampada, movimento}
            set movimento = True.
            set sensor_ativo = False.
            se movimento == True entao ligar lampada.
            se sensor_ativo != False entao desligar lampada.
        ''',

    }

    for test_name, code in tests.items():
        print(f"\n--- {test_name} ---")
        lexer.input(code)
        
        try:
            for tok in lexer:
                print(f"{tok.type:.<15} {tok.value:<20} (Linha {tok.lineno})")
        except Exception as e:
            print(f"Failed to process the lexical string: {e}")