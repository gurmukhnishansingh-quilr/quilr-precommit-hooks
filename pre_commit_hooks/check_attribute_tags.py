import yaml
import os
from collections.abc import Sequence
from collections.abc import Generator
from typing import Any
import argparse
from pathlib import Path

def getallattribute(location: str):
    attributes = {}
    for yaml_file in Path(location).rglob("*.yaml"):
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
        for attribute in data['attributes']:
            attributes[attribute.get('id')] = attribute.get('tags')
    return attributes
        

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--multi', '--allow-multiple-documents', action='store_true',
    )
    parser.add_argument(
        '--unsafe', action='store_true',
        help=(
            'Instead of loading the files, simply parse them for syntax.  '
            'A syntax-only check enables extensions and unsafe constructs '
            'which would otherwise be forbidden.  '
            'Implies --allow-multiple-documents'
        ),
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)
    all_attributes = getallattribute("./static-files/classification-config-service/attributes")
    retval = 0
    for filename in args.filenames:
        with open(filename, mode='r') as f:
            file = yaml.safe_load(f)
        if filename.find("classification-config-service/use-case/") != -1:
            for attribute in file['condition']:
                if file.get('code') in all_attributes[attribute['filter_condition']['attribute_id']]:
                    print(f"❌ Use-case {file.get('code')} is missing tags for attribute {attribute['filter_condition']['attribute_id']}")
                    return 1
    return retval