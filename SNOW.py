
    # This file defines a method to upload data into an incident ticket on SNOW

def upload_vuln_incident(snow_client, critical_vuln, lab_owner_row):


    # Defining a `Resource` for the incident API.
    incident_resource = snow_client.resource(api_path='/table/incident')

    # Put keys in SNOW table format
    snow_format = {}
    for key, val in critical_vuln.items():
        snow_format['u_' + key] = val

    # Add lab owner info to ticket
    try:
        snow_format['u_lab_owner'] = lab_owner_row['u_lab_manager_name']
    except Exception as e:
        snow_format['u_lab_owner'] = "N/A"
        print(e)

    try:
        incident_resource.create(snow_format)
    except Exception as e:
        print("FAILED TO CREATE INCIDENT: {0}".format(e))
