#!/usr/bin/env python
import sys
import os
import yaml
import uuid

def is_valid_uuid(val):
    try:
        uuid_obj = uuid.UUID(val)
        return str(uuid_obj) == val
    except ValueError:
        return False

def main():
    # Collect all YAML files in the parent directory and subdirectories
    parent_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    all_files = []

    for root, dirs, files in os.walk(parent_dir):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                all_files.append(os.path.join(root, file))

    seen_uuids = set()
    duplicate_found = False

    for filename in all_files:
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

        # Check for duplicate UUIDs across all files
        if id_value in seen_uuids:
            print(f"❌ Duplicate UUID found in {filename}: {id_value}")
            duplicate_found = True
        else:
            seen_uuids.add(id_value)

        print(f"✅ {filename} has valid and unique UUID.")

    if duplicate_found:
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())