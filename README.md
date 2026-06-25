# obsact2py

A transpiler that translates **ObsAct** (Sensor Automation Description Language) source code into executable **Python** scripts. Built with **PLY (Python Lex-Yacc)**, this project implements a LALR(1) parsing pipeline for a domain-specific language focused on home automation, device control, and sensor monitoring.

This project was developed as part of the final assignment for the **INF1022 — Analisadores Léxicos e Sintáticos** course at **PUC-Rio**.

**Arduino hardware demo:** [Watch on YouTube](https://youtube.com/shorts/UH53ignHE0I?is=ZcYn7KYEKrGa32HC)

---

## Features & Language Specification

**ObsAct** is a domain-specific language designed to manage hardware devices and sensors through declarative automation rules. A typical program consists of:

1. **Device Declarations**: defining hardware entities and their corresponding observation fields, such as `dispositivo: {Termometro, temperatura}`.
2. **State Assignments**: modifying sensor metrics or storing device states, such as `set temperatura = 40.`.
3. **Conditional Automation**: triggering actions based on logical expressions, such as `se temperatura > 30 entao ligar ventilador.`.
4. **Action Triggers & Alerts**: direct device manipulation through `ligar`, `desligar`, and `verificar`, as well as alert messages and multi-target broadcast notifications.
5. **Arduino Integration**: optional hardware execution mode that allows generated Python code to communicate with an Arduino through serial commands.

---

## Development Roadmap & Implementation Strategy

### Phase 1: Lexical Analysis

- [x] **Tokens and Regex Mappings (`lex.py`)**  
  Defined the lexical layer responsible for converting ObsAct source code into explicit token families, including reserved keywords such as `dispositivo` and `set`, logical and relational operators such as `==` and `&&`, string literals, numeric values, booleans, and identifiers.

### Phase 2: Structural Foundation & Runtime Environment

- [x] **Auxiliary Runtime (`aux.py`)**  
  Established the standard Python runtime with predefined helper functions for simulated device interaction and alert handling, including `ligar()`, `desligar()`, `verificar()`, and `alerta()`.

- [x] **Device Definitions & Basic AST Generation (`parser.py`)**  
  Implemented the initial parser rules for device declarations, observation bindings, linear assignments, and basic command nodes, producing structured Abstract Syntax Tree (AST) representations for later code generation.

### Phase 3: Advanced Semantics & Syntax Scaling

- [x] **Parameterized Alert Messages**  
  Added support for alert clauses with optional observation variables, allowing commands such as `enviar alerta ("Temperatura em", temperatura) Celular.` to be transpiled into Python alert calls with dynamic values.

- [x] **Broadcast Alert Support (`para todos:`)**  
  Extended the grammar with variable-length device target lists, allowing a single ObsAct alert command to be expanded into multiple Python `alerta()` calls, one for each target device.

- [x] **Logical Expressions & Conditional Chains**  
  Implemented relational condition parsing with chained logical expressions using `&&`, enabling ObsAct conditions to be translated into equivalent Python boolean expressions inside `if` and `else` structures.

### Phase 4: Block Handling & Code Generation

- [x] **Observation Initialization Pass**  
  Added automatic initialization for declared observations, ensuring that each observation variable starts with a default `0` value when no explicit assignment is provided before code generation.

- [x] **Indentation-Aware Conditional Blocks (`preprocessor.py` / `parser.py`)**  
  Refactored the grammar to support nested `se ... entao` blocks through synthetic `INDENT` and `DEDENT` markers, resolving ambiguous conditional grouping while keeping the ObsAct surface syntax unchanged.

- [x] **Python Code Generation (`generator.py`)**  
  Implemented AST traversal routines that convert ObsAct declarations, assignments, device actions, alerts, broadcast alerts, verification calls, and nested conditionals into executable Python code.

### Phase 5: Physical Hardware Integration

- [x] **Arduino Runtime Backend (`inoaux.py`)**  
  Implemented an alternative Python runtime capable of communicating with an Arduino board through serial communication, allowing generated ObsAct commands such as `ligar led.`, `desligar led.`, and `verificar(botao)` to interact with real hardware components.

- [x] **Serial Command Protocol**  
  Defined a lightweight communication protocol between Python and Arduino using commands such as `ON:led`, `OFF:led`, and `READ:botao`, enabling the generated Python code to control digital outputs and read physical input states.

- [x] **Continuous Execution Mode**  
  Extended the Python code generation flow to support continuous hardware monitoring through a generated `while True` loop with `time.sleep()`, allowing ObsAct programs to repeatedly read button states and update hardware outputs in real time.

- [x] **End-to-End Button-Controlled LED Demo**  
  Built and validated a complete hardware demonstration where an ObsAct program is parsed, converted into an AST, transpiled into Python, executed through `inoaux.py`, and used to control an LED connected to an Arduino digital output pin based on a physical button input.

---

## Tech Stack & Architecture

- **Host Language:** Python 3.x
- **Parsing Framework:** [PLY (Python Lex-Yacc)](https://github.com/dabeaz/ply)
- **Parsing Architecture:** LALR(1) bottom-up parser
- **Target Runtime:** Python 3.x
- **Optional Hardware Runtime:** Arduino through serial communication with `pyserial`

---

## Getting Started

### Create and activate a virtual environment

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Install the dependencies

To run the transpiler, install PLY:

```bash
pip install ply
```

For Arduino integration, also install `pyserial`:

```bash
pip install pyserial
```

If the project includes a `requirements.txt` file, you can install all dependencies with:

```bash
pip install -r requirements.txt
```

### Run the transpiler

The ObsAct source code must be written inside the `main.py` file, usually as a multiline string assigned to the `data` variable.

Example:

```python
data = '''
dispositivo: {led}
dispositivo: {botao}

se verificar(botao) == 1 entao
    ligar led.

se verificar(botao) == 0 entao
    desligar led.
'''
```

The generated Python backend can be selected through the `arduino` parameter in `generate_program()`.

For standard Python output using the simulated runtime:

```python
python_code = generate_program(ast, arduino=False)
```

For Arduino-based execution using the serial runtime:

```python
python_code = generate_program(ast, arduino=True)
```

After defining the ObsAct program and selecting the backend, run:

```bash
python3 main.py
```

This command runs the complete transpilation pipeline: reading the ObsAct source code, preprocessing indentation, performing lexical analysis, parsing the program, building the AST, and generating the equivalent Python code.

### Tests

The test cases used to validate the language are available in:

```bash
obsact2py/tests
```

They cover device declarations, assignments, conditionals, nested blocks, alerts, broadcast alerts, and Arduino integration.
