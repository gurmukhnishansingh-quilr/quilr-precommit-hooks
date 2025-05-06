import os
import sys
import yaml
import uuid

def is_valid_uuid(val):
    try:
        uuid.UUID(val)
        return True
    except Exception:
        return False

def normalize_boolean(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() == "true"
    if isinstance(value, int):
        return value == 1
    return False

def fix_yaml_file(file_path):
    with open(file_path, "r") as f:
        try:
            data = yaml.safe_load(f)
        except Exception:
            return  # Skip malformed YAML files

    if not isinstance(data, dict):
        return

    changed = False

    # Fix version
    if "version" in data and not isinstance(data["version"], str):
        original = data["version"]
        data["version"] = str(original)
        print(f"✅ Quoted version in {file_path} (was {original})")
        changed = True

    # Validate UUID
    if "id" in data and not is_valid_uuid(data["id"]):
        print(f"⚠️  Warning: Invalid UUID format in {file_path}: {data['id']}")

    # Fix top-level booleans
    for bool_field in ["disabled"]:
        if bool_field in data:
            original = data[bool_field]
            fixed = normalize_boolean(original)
            if fixed != original:
                data[bool_field] = fixed
                print(f"✅ Normalized boolean '{bool_field}' in {file_path} (was {original})")
                changed = True

    # Fix booleans in conditions
    if "condition" in data and isinstance(data["condition"], list):
        for cond in data["condition"]:
            fc = cond.get("filter_condition", {})
            for bool_field in ["editable"]:
                if bool_field in fc:
                    original = fc[bool_field]
                    fixed = normalize_boolean(original)
                    if fixed != original:
                        fc[bool_field] = fixed
                        print(f"✅ Normalized 'editable' in {file_path} (was {original})")
                        changed = True

    if changed:
        with open(file_path, "w") as f:
            yaml.dump(data, f, sort_keys=False)

def main(file_paths):
    for file_path in file_paths:
        if file_path.endswith((".yaml", ".yml")):
            fix_yaml_file(file_path)

if __name__ == "__main__":
    main(sys.argv[1:])
