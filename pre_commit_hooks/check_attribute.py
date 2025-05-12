import argparse
from collections.abc import Generator
from collections.abc import Sequence
from typing import Any
from typing import NamedTuple
import sys, os
import yaml
from pathlib import Path

def getallattribute(location: str):
    attributes = []
    for yaml_file in Path(location).rglob("*.yaml"):
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
        for attribute in data['attributes']:
            attributes.append(attribute.get('id'))
    return attributes
        
list_of_operators = [
  "is greater than",
  "is less than",
  "is equal to",
  "is not equal to",
  "is less than equal to",
  "is not in",
  "is in",
  "is_equal_to",
  "is_less_than_equal_to",
  "is_not_equal_to",
  "is_less_than",
  "is_in",
  "is_not_in"
]

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
            'which would otherwise be forbidden.  Using this option removes '
            'all guarantees of portability to other yaml implementations.  '
            'Implies --allow-multiple-documents'
        ),
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)
    retval = 0
    for filename in args.filenames:
        with open(filename, mode='r') as f:
            file = yaml.safe_load(f)
        if filename.find("classification-config-service/use-case/") != -1:
            for attribute in file['condition']:
                if attribute['filter_condition']['attribute_id'] not in getallattribute("./static-files/classification-config-service/attributes"):
                    print(f"❌ Attribute {attribute['filter_condition']['attribute_id']} in {filename} is not defined in attributes")
                    return 1
                if attribute['filter_condition']['condition'] not in list_of_operators:
                    print(f"❌ Operator {attribute['filter_condition']['condition']} in {filename} is not defined in operators")
                    return 1
        elif filename.find("quilr-playbook-service/static/execution_controls") != -1:
            for attribute in file['trigger_conditions']:
                if attribute['filter_condition']['attribute_id'] not in getallattribute("./static-files/classification-config-service/attributes"):
                    print(f"❌ Attribute {attribute['filter_condition']['attribute_id']} in {filename} is not defined in attributes")
                    return 1
                if attribute['filter_condition']['condition'] not in list_of_operators:
                    print(f"❌ Operator {attribute['filter_condition']['condition']} in {filename} is not defined in operators")
                    return 1   
    return retval


if __name__ == '__main__':
    raise SystemExit(main())