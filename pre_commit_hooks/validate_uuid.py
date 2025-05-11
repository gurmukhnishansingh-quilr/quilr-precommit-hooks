#!/usr/bin/env python
import sys
import os
import yaml
import uuid
import argparse
import re

def is_valid_uuid(val):
    try:
        uuid_obj = uuid.UUID(val)
        return str(uuid_obj) == val
    except ValueError:
        return False

def all_unique_id(path):
    ids = []
    for root, dirs, files in os.walk(os.dirname(path)):
        for file in files:
            if file != path:
                if file.endswith('.yaml') or file.endswith('.yml'):
                    with open(os.path.join(root, file), 'r') as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict):
                            ids.append(data.get('id'))
    return ids

def all_unique_code(path):
    code = []
    for root, dirs, files in os.walk(os.dirname(path)):
        for file in files:
            if file != path:
                if file.endswith('.yaml') or file.endswith('.yml'):
                    with open(os.path.join(root, file), 'r') as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict):
                            code.append(data.get('code'))
    return code

def check_code_format(code,contenttype):
    if contenttype == "action" and re.match(r'^ACT_\d+$', code):
        return True
    elif contenttype == 'use-case' and re.match(r'^UC\d+$', code):
        return True
    elif contenttype == 'behavior' and re.match(r'^BID_\d+$', code):
        return True
    elif contenttype == 'action_type' and re.match(r'^ACTP_\d+$', code):
        return True
    elif contenttype == 'attribute' and re.match(r'^ATTR_\w+_\d+$', code):
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--multi', '--allow-multiple-documents', action='store_true',
    )
    parser.add_argument(
        '--unsafe', action='store_true',
        help=(
            'Instead of loading the files, simply parse them for syntax.  '
            'A syntax-only check enables extensions and unsafe constructs '
            'which would otherwise be forbidden.  Using this option removes '
            'all guarantees of portability to other yaml implementations.  '
            'Implies --allow-multiple-documents'
        ),
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)
    parent_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    
    for filename in args.filenames:
        with open(filename, 'r') as f:
            try:
                data = yaml.safe_load(f)
            except Exception as e:
                print(f"❌ Failed to parse {filename}: {e}")
                sys.exit(1)
        # check if ID is present and valid
        id_value = data.get('id')
        code_value = data.get('code')
        if not id_value:
            print(f"❌ {filename} missing 'id' field.")
            sys.exit(1)
        if not is_valid_uuid(id_value):
            print(f"❌ {filename} has invalid UUID: {id_value}")
            sys.exit(1)
        if id_value in all_unique_id(os.dirname(filename)):
            print(f"❌ Duplicate UUID found in {filename}: {id_value}")
            sys.exit(1)
        
        # Check if the code field is present and valid
        if not code_value:
            print(f"❌ {filename} missing 'code' field.")
            sys.exit(1)
        if not check_code_format(code_value, data.get('type')):
            print(f"❌ {filename} has invalid code format: {code_value}")
            sys.exit(1)
        if code_value in all_unique_code(filename):
            print(f"❌ Duplicate code found in {filename}: {code_value}")
            sys.exit(1)

        print(f"✅ {filename} has valid and unique UUID.")

    if duplicate_found:
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())