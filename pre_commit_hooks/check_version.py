import sys
import yaml

def check_version_in_file(file_path):
    with open(file_path, "r") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"[ERROR] Failed to parse YAML in {file_path}: {e}")
            return 1

    if not data:
        print(f"[WARNING] Empty or invalid YAML in {file_path}")
        return 1

    if "version" not in data:
        print(f"[FAIL] 'version' attribute missing in {file_path}")
        return 1

    print(f"[PASS] {file_path} contains 'version'")
    return 0

def main():
    if len(sys.argv) < 2:
        print("No files provided to check.")
        return 0  # Treat as success to avoid breaking the commit for no YAML files

    exit_codes = []
    for file_path in sys.argv[1:]:
        if file_path.endswith((".yaml", ".yml")):
            exit_codes.append(check_version_in_file(file_path))

    return max(exit_codes) if exit_codes else 0

if __name__ == "__main__":
    sys.exit(main())
