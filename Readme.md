
# SAIL to CGEN Coding Challenge

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)  ![Status](https://img.shields.io/badge/Status-Completed-success)

This repository contains a Python-based solution for the SAIL to CGEN Coding Challenge, part of the LFX Mentorship program. The challenge involves converting structured YAML data into S-expressions (Scheme-like dialect) using an Intermediate Representation (IR) approach. The solution demonstrates modular data transformation, robust error handling, and comprehensive testing, serving as a precursor to the main SAIL to CGEN project, which generates CGEN descriptions for GCC from SAIL-RISC-V specifications, focusing on a tensor/matrix multiply extension.
# SAIL to CGEN Coding Challenge



This challenge prepares for the main SAIL to CGEN project, which extends the SAIL-RISC-V golden model’s Instruction Set Simulator (ISS) export to generate CGEN descriptions for GCC, supporting custom extensions like tensor/matrix multiply.

## Features
- **IR-Based Transformation**: Modular conversion from YAML to S-expressions via custom IR classes.
- **Date Handling**: Converts `YYYY-MM-DD` dates to `(make-date year month day)`.
- **Robust Error Handling**: Manages invalid YAML, missing files, and unsupported types.
- **Readable Output**: Pretty-printed S-expressions with proper indentation and quoting.
- **Comprehensive Testing**: Unit tests for scalars, dates, mappings, sequences, and edge cases.
- **Command-Line Interface**: Simple execution with `python IR.py <yaml_file>`.



## Solution Approach
The solution employs an Intermediate Representation (IR) to bridge YAML input and S-expression output:
1. **Parse YAML**: Uses `yaml.safe_load` from PyYAML to load data into Python structures, with error handling for invalid syntax or file issues.
2. **Build IR**: The `to_ir` function recursively converts data into IR classes:
   - `IRScalar`: For strings, numbers, booleans, dates, null.
   - `IRMapping`: For key-value pairs.
   - `IRSequence`: For lists.
3. **Generate S-Expression**: The `to_sexpr` function transforms IR into Scheme-like S-expressions, using `yaml:` prefixes and formatting dates as `(make-date year month day)`.



## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Mahnoor-ismail01/Yaml_To_S-Expression.git
   cd Yaml_To_S-Expression

2. Install dependencies
   ```
   pip install pyyaml

3. Run Script
   ```
   python IR.py test.yaml
4. Testing
   ```
   python -m unittest testgen.py

