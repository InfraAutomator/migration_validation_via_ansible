#!/usr/bin/env python3

import csv
import json
import sys
import os

def read_csv(file_path):
    inventory = {'ec2': {'hosts': []}, 'onprem': {'hosts': []}, '_meta': {'hostvars': {}}}
    try:
        with open(file_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ec2_ip = row.get('ec2')
                onprem_ip = row.get('onprem')
                if ec2_ip:
                    inventory['ec2']['hosts'].append(ec2_ip.strip())
                if onprem_ip:
                    inventory['onprem']['hosts'].append(onprem_ip.strip())
    except FileNotFoundError:
        print(json.dumps({}))
        sys.exit(0)
    return inventory

def main():
    if len(sys.argv) == 2 and sys.argv[1] == '--list':
        csv_file = os.path.join(os.path.dirname(__file__), 'inventory.csv')
        inventory = read_csv(csv_file)
        print(json.dumps(inventory, indent=2))
    elif len(sys.argv) == 3 and sys.argv[1] == '--host':
        # Not implemented, return empty hostvars
        print(json.dumps({}))
    else:
        print("Usage: csv_inventory.py --list | --host <hostname>")
        sys.exit(1)

if __name__ == '__main__':
    main()
