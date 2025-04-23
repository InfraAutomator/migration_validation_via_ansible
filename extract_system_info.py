import sys
import json
import os
import re

def parse_source_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = {}
    current_section = None
    section_data = []
    section_headers = set([
        "Operating System Information",
        "Logical Disk Information",
        "Mount Points Information",
        "Service Status:",
        "/etc Directory Status:",
        "/opt Directory Status:"
    ])

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip separator lines
        if line.startswith('---') or line == '':
            i += 1
            continue

        # Detect section headers
        if line in section_headers:
            if current_section and section_data:
                data[current_section] = process_section(current_section, section_data)
                section_data = []
            current_section = line.rstrip(':')
            i += 1  # Skip the '=====' line
            i += 1
            continue

        # Collect section data
        if current_section:
            section_data.append(line)
        else:
            # Parse general key-value pairs
            if ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                data[key] = value

        i += 1

    # Process the last section
    if current_section and section_data:
        data[current_section] = process_section(current_section, section_data)

    return data

def process_section(section_name, lines):
    if section_name == "Operating System Information":
        section_info = {}
        for line in lines:
            if ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                section_info[key] = value
        return section_info

    elif section_name == "Logical Disk Information":
        disks = []
        headers = []
        for line in lines:
            if not headers:
                headers = re.split(r'\s{2,}|\t', line.strip())
                continue
            values = re.split(r'\s{2,}|\t', line.strip())
            if len(values) == len(headers):
                disk_info = dict(zip(headers, values))
                disks.append(disk_info)
        return disks

    elif section_name in ["Mount Points Information", "Service Status"]:
        return lines  # Return as a list of lines

    elif section_name in ["/etc Directory Status", "/opt Directory Status"]:
        files = []
        for line in lines:
            parts = line.split()
            if len(parts) == 2:
                files.append(parts[1])
        return files

    else:
        return lines  # Default case

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_system_info.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    parsed_data = parse_source_file(input_file)

    with open(output_file, "w") as json_file:
        json.dump(parsed_data, json_file, indent=4)
