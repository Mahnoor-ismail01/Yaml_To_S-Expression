import yaml
from datetime import datetime, date
import re
import sys


class IRScalar:
    def __init__(self, value, is_date=False):
        self.value = value
        self.is_date = is_date

class IRMapping:
    def __init__(self, mapping):
        self.mapping = mapping

class IRSequence:
    def __init__(self, sequence):
        self.sequence = sequence

def to_ir(data):
    if isinstance(data, dict):
        return IRMapping({key: to_ir(value) for key, value in data.items()})
    elif isinstance(data, list):
        return IRSequence([to_ir(item) for item in data])
    elif isinstance(data, str):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', data):
            try:
                datetime.strptime(data, "%Y-%m-%d")
                return IRScalar(data, is_date=True)
            except ValueError:
                pass
        return IRScalar(data)
    elif isinstance(data, date):
        return IRScalar(data, is_date=True)
    elif isinstance(data, (int, float, bool)):
        return IRScalar(data)
    elif data is None:
        return IRScalar(None)
    else:
        raise ValueError(f"Unsupported data type: {type(data)}")


def to_sexpr(ir, indent=0):
    indent_str = "  " * indent
    
    if isinstance(ir, IRScalar):
        if ir.is_date:
            if isinstance(ir.value, date):
                return f"(make-date {ir.value.year} {ir.value.month:02d} {ir.value.day:02d})"
            else:
                parsed_date = datetime.strptime(ir.value, "%Y-%m-%d")
                return f"(make-date {parsed_date.year} {parsed_date.month:02d} {parsed_date.day:02d})"
        elif isinstance(ir.value, bool):
            return "true" if ir.value else "false"
        elif isinstance(ir.value, str):
            return f'"{ir.value.replace('"', '\\"')}"'
        elif isinstance(ir.value, (int, float)):
            return str(ir.value)
        elif ir.value is None:
            return "null"
    
    elif isinstance(ir, IRMapping):
        if not ir.mapping:
            return f"{indent_str}()"
        items = []
        for key, value in ir.mapping.items():
            value_str = to_sexpr(value, indent + 1)
            items.append(f"{indent_str}(yaml:{key} {value_str})")
        if indent == 0 and len(ir.mapping) == 1:
            return items[0]
        if indent == 0:
            return "(" + "\n" + "\n".join(items) + "\n)"
        return "\n".join(items)
    
    elif isinstance(ir, IRSequence):
        if not ir.sequence:
            return f"{indent_str}()"
        items = [to_sexpr(item, indent + 1) for item in ir.sequence]
        return f"{indent_str}(" + "\n" + "\n".join(items) + "\n" + indent_str + ")"
    
    else:
        raise ValueError(f"Unsupported IR type: {type(ir)}")

def convert_to_sexpr(yaml_file):
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        if data is None:
            return "null"
        return to_sexpr(to_ir(data))
    except yaml.YAMLError as e:
        return f"Error parsing YAML: {e}"
    except FileNotFoundError:
        return f"Error: File {yaml_file} not found"
    except Exception as e:
        return f"Error reading file: {e}"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python IR.py <yaml_fileInput>")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    result = convert_to_sexpr(yaml_file)
    
    if result.startswith("Error"):
        print(result)
        sys.exit(1)
    
    with open("output.scm", "w") as f:
        f.write(result)