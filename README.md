# Flora Interpreter

## Overview

Flora Interpreter is a simple nature-inspired interpreter developed in Python. It processes source code written in the Flora programming language, which uses botanical and environmental keywords to represent programming constructs.

The interpreter performs lexical analysis, syntax validation, and program execution. It also generates files containing the source code without unnecessary whitespace and a list of reserved words and symbols detected in the program.

---

## Features

* Variable declarations
* Variable assignments
* Arithmetic operations
* Output statements
* Conditional statements using `branch`
* Lexical analysis
* Syntax checking
* Program execution
* Generation of `NOSPACES.TXT`
* Generation of `RES_SYM.TXT`

---

## Data Types

| Data Type | Description           |
| --------- | --------------------- |
| root      | Integer values        |
| dew       | Floating-point values |
| petal     | String values         |

---

## Reserved Words

```text
sprout
root
dew
petal
bloom
branch
```

---

## Supported Operators

### Arithmetic Operators

```text
+
-
*
/
```

### Comparison Operators

```text
<
>
==
!=
```

---

## Sample Flora Program

```text
sprout root trees = 15;
sprout dew rainfall = 12.5;
sprout petal forest = "Mangrove";

bloom forest;

branch(trees > 10)
bloom "Forest is thriving";
```

### Expected Output

```text
Mangrove
Forest is thriving
```

---

## Running the Program

1. Place your Flora source code in a `.flora` file.
2. Run the interpreter:

```bash
python flora.py
```

3. The interpreter will:

   * Read the source file
   * Remove unnecessary whitespace
   * Generate `NOSPACES.TXT`
   * Generate `RES_SYM.TXT`
   * Validate syntax
   * Execute the program
   * Display any errors found

---

## Project Limitations

* `branch` controls only one following statement.
* `else` statements are not supported.
* Block statements are not supported.
* Keywords are case-sensitive.
* Only `root`, `dew`, and `petal` data types are supported.

---

## Developed Using

* Python 3
* File Handling
* Regular Expressions (Regex)
* Basic Interpreter Concepts
