import ply.yacc as yacc
from lex import tokens

def p_program(p):
    '''PROGRAM : DEVICES CMDS'''
    p[0] = {'type': 'program', 'devices': p[1], 'commands': p[2]}

# -- DEVICE RULES -- 

def p_devices_single(p):
    '''DEVICES : DEVICE'''
    p[0] = [p[1]]

def p_devices_multiple(p):
    '''DEVICES : DEVICE DEVICES'''
    p[0] = [p[1]] + p[2]

def p_device_simple(p):
    '''DEVICE : DISPOSITIVO COLON LBRACE ID RBRACE'''
    p[0] = {'type': 'declaration', 'device_name': p[4], 'observation': None}

def p_device_obs(p):
    '''DEVICE : DISPOSITIVO COLON LBRACE ID COMMA ID RBRACE'''
    p[0] = {'type': 'declaration', 'device_name': p[4], 'observation': p[6]}

# -- CMD RULES --

def p_cmds_multiple(p):
    '''CMDS : CMD CMDS'''
    p[0] = [p[1]] + p[2]

def p_cmds_single(p):
    '''CMDS : CMD'''
    p[0] = [p[1]]

def p_cmd_type(p):
    '''CMD : ATTRIB DOT
           | OBSACT
           | ACT DOT'''
    p[0] = p[1]

# -- ATTRIB & ACT ---

def p_attrib(p):
    '''ATTRIB : SET ID ASSIGN VAR'''
    p[0] = {'type': 'assignment', 'var': p[2], 'value': p[4]}

def p_var(p):
    '''VAR : NUM
           | BOOL'''
    p[0] = p[1]

def p_attrib_actexe(p):
    '''ATTRIB : SET ID ASSIGN ACTEXECUTE'''
    p[0] = {'type': 'assignment', 'var': p[2], 'value': p[4]}

def p_act(p):
    '''ACT : ACTEXECUTE
           | ACTALERT'''
    p[0] = p[1]

def p_action(p):
    '''ACTION : LIGAR
              | DESLIGAR'''
    p[0] = p[1]

def p_act_execute(p):
    '''ACTEXECUTE : ACTION ID'''
    p[0] = {'type': 'execute', 'action': p[1], 'target': p[2]}


def p_act_alert_simple(p):
    '''ACTALERT : ENVIAR ALERTA LPAREN STRING RPAREN ID'''
    p[0] = {'type': 'alert', 'message': p[4], 'var_obs': None, 'target': p[6]}

def p_act_alert_var(p):
    '''ACTALERT : ENVIAR ALERTA LPAREN STRING COMMA ID RPAREN ID'''
    p[0] = {'type': 'alert', 'message': p[4], 'var_obs': p[6], 'target': p[8]}


def p_verify_call(p):
    '''VERIFYCALL : VERIFICAR LPAREN ID RPAREN'''
    p[0] = {'type': 'verify', 'target': p[3]}

def p_attrib_verify(p):
    '''ATTRIB : SET ID ASSIGN VERIFYCALL'''
    p[0] = {'type': 'assignment', 'var': p[2], 'value': p[4]}

# -- Condicionais --

def p_obsact_if(p):
    '''OBSACT : SE OBS ENTAO CMDS'''
    p[0] = {'type': 'conditional_if', 'condition': p[2], 'commands_0': p[4]}

def p_obsact_if_else(p):
    '''OBSACT : SE OBS ENTAO CMDS SENAO CMDS'''
    p[0] = {'type': 'conditional_if_else', 'condition': p[2], 'commands_0': p[4], 'commands_1': p[6]}

def p_obs_simple(p):
    '''OBS : ID oplogic VAR'''
    p[0] = {'left': p[1], 'oplogic': p[2], 'right': p[3]}

def p_obs_verify(p):
    '''OBS : VERIFYCALL oplogic VAR'''
    p[0] = {'left': p[1], 'oplogic': p[2], 'right': p[3]}

def p_obs_verify_and(p):
    '''OBS : VERIFYCALL oplogic VAR AND OBS'''
    p[0] = {'left': p[1], 'oplogic': p[2], 'right': p[3], 'and': p[5]}

def p_obs_and(p):
    '''OBS : ID oplogic VAR AND OBS'''
    p[0] = {'left': p[1], 'oplogic': p[2], 'right': p[3], 'and': p[5]}

def p_oplogic(p):
    '''oplogic : GT
               | LT
               | GE
               | LE
               | EQ
               | NEQ'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo a '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe no final do arquivo")

parser = yacc.yacc()


if __name__ == '__main__':
    import json

    tests = {
        "Teste 1: Programa mínimo com dispositivo e ação": '''
            dispositivo: {ventilador}
            ligar ventilador.
        ''',

        "Teste 2: Declaração com observation e atribuição numérica": '''
            dispositivo: {Termometro, temperatura}
            set temperatura = 40.
        ''',

        "Teste 3: Booleano em atribuição": '''
            dispositivo: {lampada, movimento}
            set movimento = True.
        ''',

        "Teste 4: Condicional simples com número": '''
            dispositivo: {Termometro, temperatura}
            dispositivo: {ventilador}
            set temperatura = 40.
            se temperatura > 30 entao ligar ventilador.
        ''',

        "Teste 5: Condicional simples com booleano": '''
            dispositivo: {lampada, movimento}
            set movimento = True.
            se movimento == True entao ligar lampada.
        ''',

        "Teste 6: Condicional com senao": '''
            dispositivo: {lampada, movimento}
            set movimento = False.
            se movimento == True entao ligar lampada. senao desligar lampada.
        ''',

        "Teste 7: Operador lógico AND com número e booleano": '''
            dispositivo: {lampada, movimento}
            dispositivo: {Termometro, temperatura}
            set movimento = True.
            set temperatura = 35.
            se temperatura > 30 && movimento == True entao ligar lampada.
        ''',

        "Teste 8: Alerta simples com mensagem": '''
            dispositivo: {Celular}
            enviar alerta ("Hora de acordar!") Celular.
        ''',

        "Teste 9: Alerta com concatenação de observation": '''
            dispositivo: {Termometro, temperatura}
            set temperatura = 37.
            enviar alerta ("Temperatura esta em", temperatura) Termometro.
        ''',

        "Teste 10: Bloco condicional com múltiplos comandos": '''
            dispositivo: {Termometro, temperatura}
            dispositivo: {ventilador, potencia}
            dispositivo: {Celular}

            set temperatura = 40.

            se temperatura > 30 entao
                ligar ventilador.
                set potencia = 90.
                enviar alerta ("Temperatura alta", temperatura) Celular.
        ''',

        "Teste 11: Condicional aninhado": '''
            dispositivo: {Termometro, temperatura}
            dispositivo: {ventilador, potencia}

            set temperatura = 40.
            set potencia = 0.

            se temperatura > 30 entao
                ligar ventilador.
                se potencia == 0 entao set potencia = 90.
        ''',

        "Teste 12: Verificar em atribuição": '''
            dispositivo: {ventilador}
            set estado_ventilador = verificar(ventilador).
        ''',

        "Teste 13: Verificar dentro de condição": '''
            dispositivo: {umidificador}
            se verificar(umidificador) == 0 entao ligar umidificador.
        ''',

        "Teste 14: Verificar com AND": '''
            dispositivo: {umidificador}
            dispositivo: {sensor, umidade}

            set umidade = 35.

            se verificar(umidificador) == 0 && umidade < 40 entao ligar umidificador.
        ''',

        "Teste 15: Operadores lógicos completos": '''
            dispositivo: {sensor, valor}
            dispositivo: {atuador}

            set valor = 10.

            se valor > 5 entao ligar atuador.
            se valor < 20 entao desligar atuador.
            se valor >= 10 entao ligar atuador.
            se valor <= 10 entao desligar atuador.
            se valor == 10 entao ligar atuador.
            se valor != 0 entao desligar atuador.
        ''',

        "Teste 16: Programa maior misturando recursos": '''
            dispositivo: {Termometro, temperatura}
            dispositivo: {lampada, movimento}
            dispositivo: {ventilador, potencia}
            dispositivo: {Celular}

            set temperatura = 41.
            set movimento = True.
            set potencia = 0.

            se temperatura > 30 && movimento == True entao
                ligar ventilador.
                set potencia = 90.
                enviar alerta ("Temperatura detectada", temperatura) Celular.

            se movimento == False entao desligar lampada. senao ligar lampada.
        ''',

        "Teste 17: Broadcast simples": '''
            dispositivo: {monitor}
            dispositivo: {celular}
            dispositivo: {tablet}

            enviar alerta ("Sistema iniciado") para todos: monitor, celular, tablet.
        ''',

        "Teste 18: Broadcast com concatenação": '''
            dispositivo: {monitor}
            dispositivo: {celular}
            dispositivo: {Termometro, temperatura}

            set temperatura = 39.
            enviar alerta ("Temperatura em", temperatura) para todos: monitor, celular.
        ''',

        "Teste 19: Erro esperado - comando sem ponto": '''
            dispositivo: {lampada}
            ligar lampada
        ''',

        "Teste 20: Erro esperado - booleano inválido em minúsculo": '''
            dispositivo: {lampada, movimento}
            set movimento = true.
        ''',

        "Teste 21: Erro esperado - ligar usado como expressão de condição": '''
            dispositivo: {lampada}
            se ligar lampada == 1 entao desligar lampada.
        '''
    }

    for test_name, code in tests.items():
        print(f"\n{'=' * 80}")
        print(test_name)
        print(f"{'=' * 80}")

        try:
            result = parser.parse(code)

            if result is None:
                print("Resultado: ERRO ou AST nula")
            else:
                print("Resultado: OK")
                print(json.dumps(result, indent=2, ensure_ascii=False))

        except Exception as e:
            print(f"Falha ao processar parser: {e}")