import sys
import yaml
import jsonschema
from jsonschema import validate

# Define JSON Schema for type == "use-case"
use_case_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "version": {"type": "float"},
        "code": {"type": "string"},
        "name": {"type": "string"},
        "type": {"type": "string", "enum": ["use-case"]},
        "description": {"type": "string"},
        "posture": {"type": "array", "items": {"type": "string"}},
        "behavior": {"type": "array", "items": {"type": "string"}},
        "condition": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "operator": {"type": ["string", "null"]},
                    "filter_condition": {
                        "type": "object",
                        "properties": {
                            "attribute_type": {"type": "string"},
                            "attribute_id": {"type": "string"},
                            "condition": {"type": "string"},
                            "value": {"type": "string"},
                            "filter_group": {"type": ["string", "null"]},
                            "editable": {"type": "boolean"}
                        },
                        "required": ["attribute_type", "attribute_id", "condition", "value", "editable"]
                    }
                },
                "required": ["filter_condition"]
            }
        },
        "disabled": {"type": "boolean"},
        "createdon": {"type": "integer"},
        "updatedon": {"type": "integer"}
    },
    "required": ["id", "version", "code", "name", "type", "description", "posture", "behavior", "condition", "disabled", "createdon", "updatedon"]
}

def main():
    for filename in sys.argv[1:]:
        with open(filename, 'r') as f:
            try:
                data = yaml.safe_load(f)
            except Exception as e:
                print(f"❌ Failed to parse {filename}: {e}")
                sys.exit(1)

            if not isinstance(data, dict):
                print(f"❌ {filename} is not a valid YAML object.")
                sys.exit(1)

            if data.get("type") != "use-case":
                print(f"🔁 Skipping {filename} (type != use-case)")
                continue

            try:
                validate(instance=data, schema=use_case_schema)
                print(f"✅ {filename} is valid")
            except jsonschema.exceptions.ValidationError as e:
                print(f"❌ {filename} failed validation:\n{e.message}")
                sys.exit(1)

if __name__ == "__main__":
    main()
