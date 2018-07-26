import pysnow
import nexpose
import json
from lab_owners_snow import get_lab_owner_by_ip

config_file_path = 'C:\\nexposeCreds.json'
with open(config_file_path, 'r') as f:
    config = json.load(f)
    report = nexpose.generate_report(config)

    found_owners = {}

    # ip_address
    for vuln in report:
        # each 'vuln' is a python dict
        ip = vuln['ip_address']

        # Get all lab owners this IP might belong to
        if 'ip' not in found_owners:
            lab_owner_row = get_lab_owner_by_ip(ip)
            # Add found lab owner to dict for quick lookups
            found_owners[ip] = lab_owner_row
        else:
            lab_owner_row = found_owners[ip]

        print(lab_owner_row)
        exit(0)
