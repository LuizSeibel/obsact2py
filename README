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

To ensure absolute stability, the compiler is built incrementally using a test-driven approach, scaling from core low-level mechanics to advanced syntax transformations.

### Phase 1: Lexical Analysis 
- [x] **Tokens and Regex Mappings (`lex.py`)** Deconstruction of source streams into explicit terminal families (keywords like `dispositivo`, `set`, operators like `==`, `&&`, string literals, and identifiers). Implemented using PLY reflection.

### Phase 2: Structural Foundation & Environment 
- [x] **Boilerplate and Auxiliary Runtime (`aux.py`)** Establishing the targeted execution runtime containing predefined Python wrappers for `ligar()`, `desligar()`, `verificar()`, and `alerta()`.
- [ ] **Device Definitions & Basic AST Generation** Building the core parser rules to construct Abstract Syntax Tree (AST) sub-nodes from basic `DEVICE` and simple linear `set` assignments.

### Phase 3: Advanced Semantics & Syntax Scaling 
- [ ] **String Concatenation Rules** Handling embedded evaluations in communication semantics, automatically unpacking pairs of string constants and variable identifiers inside alert clauses.
- [ ] **Broadcast Architecture (`para todos:`)** Expanding the grammatic definitions to support variable-length identifier collections, emitting deterministic execution loops to map single instructions across plural targets.
- [ ] **Logical Expressions & Precedences** Integrating relational sub-trees with conditional chaining operators (`&&`), carefully balancing shifting boundaries to cleanly emit standard Python `if/elif/else` structures.

### Phase 4: Symbol Tracking & Optimization 
- [ ] **Zero-Initialization Symbol Table** Enforcing a compiler-level safeguard that tracks all declared observations across the compilation context, automatically injecting a default `0` assignment for variables that lack explicit initialization.
- [ ] **Grammar Optimization & LALR(1) Convergence (`parser.py`)** Refactoring grammar rules to prevent left-recursion loops and resolve Shift/Reduce ambiguities native to conditional branches.

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