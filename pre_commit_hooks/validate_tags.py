import os
import sys
import yaml

# Path to the use case folder
USE_CASE_FOLDER = "/Users/gurjeet-quilr/Desktop/dev-folder/content-management-service/static-files/classification-config-service/use_case"

def load_tags_from_use_case(tag):
    # Search for the tag in all use case files
    for root, dirs, files in os.walk(USE_CASE_FOLDER):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    data = yaml.safe_load(f)
                    if data and 'tags' in data:
                        if tag in data['tags']:
                            return True
    return False

def main():
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        data = yaml.safe_load(f)

    if not data or 'tags' not in data or data['tags'] is None:
        print(f"No tags found in {filename}")
        sys.exit(0)

    # Ensure data['tags'] is a list
    tags = data['tags']
    if not isinstance(tags, list):
        print(f"Invalid 'tags' format in {filename}")
        sys.exit(1)

    for tag in tags:
        if not load_tags_from_use_case(tag):
            print(f"Tag '{tag}' in {filename} does not exist in use case folder.")
            sys.exit(1)

    print(f"All tags in {filename} are valid.")
    sys.exit(0)

if __name__ == "__main__":
    main()