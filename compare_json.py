import json
import sys
from json_dict_diff import diff  # Ensure you have installed this library

# Define keys to ignore or exclusively compare
IGNORE_KEYS = []  # e.g., ['Date', 'MemTotal']
ONLY_KEYS = ['System Name']    # e.g., ['System Name', 'Operating System Information']

def load_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None

def get_comparison_keys(source_keys, target_keys):
    # Determine the set of keys to compare
    if ONLY_KEYS:
        keys_to_compare = set(ONLY_KEYS)
    else:
        keys_to_compare = set(source_keys) | set(target_keys)
    keys_to_compare -= set(IGNORE_KEYS)
    return keys_to_compare

def filter_json(json_data, keys_to_compare):
    return {k: json_data[k] for k in keys_to_compare if k in json_data}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_json.py <source.json> <target.json>")
        sys.exit(1)

    source_file = sys.argv[1]
    target_file = sys.argv[2]

    source_json = load_json(source_file)
    target_json = load_json(target_file)

    if source_json is None or target_json is None:
        print("Comparison failed due to load error.")
        sys.exit(1)

    # Determine keys to compare
    comparison_keys = get_comparison_keys(source_json.keys(), target_json.keys())

    # Filter JSONs based on comparison keys
    source_filtered = filter_json(source_json, comparison_keys)
    target_filtered = filter_json(target_json, comparison_keys)

    # Compute the diff
    differences = diff(source_filtered, target_filtered)

    if differences:
        print("Server configuration do not match. Differences:")
        print(json.dumps(differences, indent=4))
        sys.exit(1)
    else:
        print("Server configuration match.")
        sys.exit(0)
