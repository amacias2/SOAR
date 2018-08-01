import nexpose
import json
import lab_owners_snow
import SNOW

    # This file uses the method created in lab_owners_snow to get the match and then populate the data into a SNOW incident ticket using the method defined in SNOW.

config_file_path = '<>'
with open(config_file_path, 'r') as f:
    config = json.load(f)
    #pylint: disable-msg=R0913
    #pylint: disable-msg=too-many-arguments
    report = nexpose.generate_report(config)
    snow_client = lab_owners_snow.get_snow_client()

    found_owners = {}

    # ip_address
    for vuln in report:
        try:
            # each 'vuln' is a python dict
            ip = vuln['ip_address']
            print("IP: {0}".format(ip))

            # Get all lab owners this IP might belong to
            if ip not in found_owners:
                lab_owner_row = lab_owners_snow.get_lab_owner_by_ip(snow_client, ip)
                # Add found lab owner to dict for quick lookups
                found_owners[ip] = lab_owner_row
            else:
                lab_owner_row = found_owners[ip]

            print("LAB OWNER: {0}".format(lab_owner_row))

            # Upload vuln incident to SNOW
            print("UPLOADING TO SNOW")
            SNOW.upload_vuln_incident(snow_client, vuln, lab_owner_row)

        except Exception as e:
            print(e)

