import sys
import subprocess
import yaml
from packaging import version

# Get the file path passed as an argument
file_path = sys.argv[1]

# Function to get the version from a YAML content
def extract_version(yaml_content):
    data = yaml.safe_load(yaml_content)
    return data.get("version")

# Read the old (last committed) file using 'git show'
def get_old_version(file_path):
    try:
        old_content = subprocess.check_output(
            ["git", "show", f"HEAD:{file_path}"], stderr=subprocess.DEVNULL
        )
        return extract_version(old_content)
    except subprocess.CalledProcessError:
        # File might be new (not in previous commit)
        return None

# Read the new (staged) version of the file using 'git show :<file>'
def get_new_version(file_path):
    try:
        new_content = subprocess.check_output(
            ["git", "show", f":{file_path}"], stderr=subprocess.DEVNULL
        )
        return extract_version(new_content)
    except subprocess.CalledProcessError:
        print(f"Error reading staged version of {file_path}")
        sys.exit(1)

def main():
    old_ver = get_old_version(file_path)
    new_ver = get_new_version(file_path)

    # If no old version, allow commit (new file)
    if old_ver is None:
        print(f"{file_path} is a new file. Skipping version check.")
        return

    # Compare versions using packaging.version
    if version.parse(str(new_ver)) <= version.parse(str(old_ver)):
        print(f"❌ Version check failed: {new_ver} is not greater than {old_ver}")
        sys.exit(1)

    print(f"✅ Version check passed: {new_ver} > {old_ver}")

if __name__ == "__main__":
    main()
