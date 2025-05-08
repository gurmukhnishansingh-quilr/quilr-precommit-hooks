import sys  # Imports the sys module to interact with the Python interpreter, used for exiting with status codes.
import os   # Imports the os module for operating system interactions (not used in current code but imported).
import re   # Imports the re module for regular expressions (not used in current code but imported).
import uuid # Imports the uuid module to generate and validate UUIDs.
import yaml # Imports the yaml module to parse YAML files.
from glob import glob  # Imports the glob function to find files matching a pattern recursively.

def is_valid_uuid(val):
    # Defines a function to check if a string is a valid UUID.
    try:
        uuid_obj = uuid.UUID(val)  # Attempts to create a UUID object from the string.
        return str(uuid_obj) == val  # Checks if the string representation matches the original input.
    except ValueError:
        return False  # If an exception occurs, the string is not a valid UUID, return False.

def main():
    # Main function to perform validation across files.
    # Collects all YAML files in the specified directory and subdirectories.
    files = glob('content-management-service/static-files/**/*.yaml', recursive=True)
    # Creates an empty set to store unique UUIDs found.
    ids = set()
    # Creates an empty set to track duplicate UUIDs (not used further in current code).

    for filename in files:
        # Loop through each YAML file found.
        with open(filename, 'r') as f:
            # Opens the current file for reading.
            try:
                data = yaml.safe_load(f)  # Parses the YAML content into a Python dictionary.
            except Exception as e:
                # If parsing fails, print an error message.
                print(f"Error parsing {filename}: {e}")
                continue  # Skip to the next file.

            if not data or 'id' not in data:
                # If the file is empty or doesn't contain an 'id' key, skip it.
                continue

            id_value = data['id']
            # Extracts the 'id' value from the YAML data.

            # Validate UUID format.
            if not is_valid_uuid(id_value):
                # If the 'id' is not a valid UUID, print an error message.
                print(f"Invalid UUID format in {filename}: {id_value}")
                return 1  # Exit with status 1 indicating failure.

            # Check for duplicate UUIDs.
            if id_value in ids:
                # If the UUID has already been seen, it's a duplicate.
                print(f"Duplicate UUID found in {filename}: {id_value}")
                return 1  # Exit with status 1 indicating failure.
            ids.add(id_value)  # Add the valid, unique UUID to the set.

    # If all files are processed without errors, print success message.
    print("All UUIDs are valid and unique.")
    return 0  # Exit with status 0 indicating success.

if __name__ == "__main__":
    # Entry point of the script.
    sys.exit(main())  # Runs the main function and exits with its return code.