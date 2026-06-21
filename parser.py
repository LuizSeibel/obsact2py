import ply.yacc as yacc
from lex import tokens

def p_program(p):
    '''PROGRAM : DEVICES CMDS'''
    p[0] = {'tipo': 'programa', 'dispositivos': p[1], 'comandos': p[2]}

# -- Devices rules -- 

def p_devices_single(p):
    '''DEVICES : DEVICE'''
    p[0] = [p[1]]

def p_devices_multiple(p):
    '''DEVICES : DEVICE DEVICES'''
    p[0] = [p[1]] + p[2]

def p_device_simple(p):
    '''DEVICE : DISPOSITIVO COLON LBRACE ID RBRACE'''
    p[0] = {'tipo': 'declaracao', 'nome_dispositivo': p[4], 'observacao': None}

def p_device_obs(p):
    '''DEVICE : DISPOSITIVO COLON LBRACE ID COMMA ID RBRACE'''
    p[0] = {'tipo': 'declaracao', 'nome_dispositivo': p[4], 'observacao': p[6]}

# -- CMD RULES --

def p_cmds_multiple(p):
    '''CMDS : CMD DOT CMDS'''
    p[0] = [p[1]] + p[3]

def p_cmds_single(p):
    '''CMDS : CMD DOT'''
    p[0] = [p[1]]

def p_cmd_type(p):
    '''CMD : ATTRIB
           | OBSACT
           | ACT'''
    p[0] = p[1]

