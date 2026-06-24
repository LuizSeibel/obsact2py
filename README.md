# obsact2py

A transpiler that translates **ObsAct** (Sensor Automation Description Language) source code into executable **Python** scripts. Built using **PLY (Python Lex-Yacc)**, this project implements a complete LALR(1) parsing architecture to parse domain-specific language rules for home automation and sensor monitoring.

This project was developed as part of the final assignment for the **INF1022 (ANALIS LEXICOS E SINTATICOS)** course at **PUC-Rio**.

---

## Features & Language Specification
**ObsAct** is a domain-specific language designed to manage hardware devices and sensors through declarative rules. A typical program consists of:
1. **Device Declarations**: Defining hardware entities and their corresponding observation fields (e.g., `dispositivo: {Termometro, temperatura}`).
2. **State Assignments**: Modifying sensor metrics or capturing state values (e.g., `set temperatura = 40.`).
3. **Conditional Automation**: Triggering actions based on rich logical expressions (e.g., `se temperatura > 30 entao ligar ventilador.`).
4. **Action Triggers & Alerts**: Direct device manipulation (`ligar`, `desligar`, `verificar`) and complex messaging systems (including single-target and multi-target broadcast notifications).

---

## Development Roadmap & Implementation Strategy

### Phase 1: Lexical Analysis 
- [x] **Tokens and Regex Mappings (`lex.py`)** 
    Defined the lexical layer responsible for converting ObsAct source code into explicit token families, including reserved keywords such as dispositivo and set, logical and relational operators such as == and &&, string literals, numeric values, booleans, and identifiers.

### Phase 2: Structural Foundation & Environment 
- [x] **Boilerplate and Auxiliary Runtime (`aux.py`)** 
    Established the target Python runtime with predefined helper functions for device interaction and alert handling, including ligar(), desligar(), verificar(), and alerta().
- [x] **Device Definitions & Basic AST Generation(`parser.py`)**
    Implemented the initial parser rules for device declarations, observation bindings, linear assignments, and basic command nodes, producing structured Abstract Syntax Tree (AST) representations for later code generation.

### Phase 3: Advanced Semantics & Syntax Scaling 
- [x] **Parameterized Alert Messages**
    Added support for alert clauses with optional observation variables, allowing commands such as enviar alerta ("Temperatura em", temperatura) Celular. to be transpiled into Python alert calls with dynamic values.
- [x] **Broadcast Alert Support (`para todos:`)**
    Extended the grammar with variable-length device target lists, allowing a single ObsAct alert command to be expanded into multiple Python alerta() calls, one for each target device.
- [x] **Logical Expressions & Conditional Chains**
    Implemented relational condition parsing with chained logical expressions using &&, enabling ObsAct conditions to be translated into equivalent Python boolean expressions inside if and else structures.

### Phase 4: Symbol Tracking & Optimization 
- [x] **Observation Initialization Pass**
    Added automatic initialization for declared observations, ensuring that each observation variable starts with a default 0 value when no explicit assignment is provided before code generation.
- [x] **Indentation-Aware Conditional Blocks (`parser.py`)**
    Refactored the grammar to support nested se ... entao blocks through synthetic INDENT and DEDENT markers, resolving ambiguous conditional grouping while keeping the ObsAct surface syntax unchanged.
- [x] **Python Code Generation (`generator.py`)**
    Implemented AST traversal routines that convert ObsAct declarations, assignments, device actions, alerts, broadcast alerts, verification calls, and nested conditionals into executable Python code.

### Phase 5: Physical Hardware Integration
- [ ] **Arduino Runtime Integration (`arduino_aux.py`)**  
  Extend the generated Python runtime to communicate with an Arduino board through serial communication, enabling ObsAct commands such as `ligar led.` and `desligar led.` to control a real LED circuit.

- [ ] **Device-to-Pin Mapping**  
  Add a hardware mapping layer that associates declared ObsAct devices with Arduino digital pins, allowing device names from the language to be translated into physical outputs.

- [ ] **Serial Command Protocol**  
  Define a simple communication protocol between Python and Arduino, using commands such as `ON:led`, `OFF:led`, or `READ:sensor` to trigger physical behavior from generated Python code.

- [ ] **End-to-End Hardware Demo**  
  Build a complete ObsAct program that declares an LED device, transpiles the source code to Python, sends commands to Arduino, and physically turns the LED on or off.
---

## Tech Stack & Architecture

- **Host Language:** Python 3.x
- **Parsing Framework:** [PLY (Python Lex-Yacc)](https://github.com/dabeaz/ply)
- **Parsing Architecture:** LALR(1) Ascending Parser
- **Target Runtime Environment:** Python 3.x (Modular scripts interacting with a standard I/O pseudolayer)

---

## Getting Started

```bash
pip install ply
```