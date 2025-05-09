#!/usr/bin/env python
import sys
import yaml
import uuid

def is_valid_uuid(val):
    try:
        uuid_obj = uuid.UUID(val)
        return str(uuid_obj) == val
    except ValueError:
        return False

def main():
    seen_uuids = set()
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

        id_value = data.get('id')
        if not id_value:
            print(f"❌ {filename} missing 'id' field.")
            sys.exit(1)

        # Check if UUID is valid
        if not is_valid_uuid(id_value):
            print(f"❌ {filename} has invalid UUID: {id_value}")
            sys.exit(1)

        # Check for duplicate UUIDs
        if id_value in seen_uuids:
            print(f"❌ Duplicate UUID found in {filename}: {id_value}")
            sys.exit(1)
        else:
            seen_uuids.add(id_value)

        print(f"✅ {filename} has valid and unique UUID.")

if __name__ == "__main__":
    sys.exit(main())