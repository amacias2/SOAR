import pysnow
import json
import os
from netaddr import *

    # This file creates the method get_lab_owner_by_ip which matches lab to lab owner by IP

#Variables
client_ID = '<>'
instance = '<>'
word_of_pass= '<>'
store = {'token': None}

# Takes care of refreshing the token storage if needed
def updater(new_token):
    print("OAuth token refreshed!")
    store['token'] = new_token


def get_snow_client():
    global word_of_pass

    # Create the OAuthClient with the ServiceNow provided `client_id` and `client_secret`, and a `token_updater`
    # function which takes care of refreshing local token storage.
    client = pysnow.OAuthClient(client_id=client_ID, client_secret=word_of_pass,
                                token_updater=updater, instance=instance)

    if os.path.exists('token'):
        with open('token', 'r') as f:
            store['token'] = json.load(f)

    else:
        # No previous token exists. Generate new.
        username = raw_input("Enter Username: ")
        word_of_pass = raw_input("Enter Password: ")
        store['token'] = client.generate_token(username, word_of_pass)
        # print (store['token'])
        with open('token', 'w') as f:
            f.write(json.dumps(store['token']))

    # Set the access / refresh tokens
    client.set_token(store['token'])

    return client


def get_lab_owner_by_ip(snow_client, ip_address):
    # First three octet's are stored now under the variable name class_c_address
    class_c_address = ".".join(ip_address.split(".")[0:3])

    # Defining a `Resource` for the incident API.
    lab_owner_resource = snow_client.resource(api_path='/table/u_lab_owners')

    # Query incident records based on subnets in the lab owner table in SNOW
    qb = (
        pysnow.QueryBuilder().field('u_subnet').contains(class_c_address)
    )
    response = lab_owner_resource.get(query=qb, stream=True)

    # Check all (filtered) lab owner ranges for IP address
    for potential_lab_owner_row in response.all():

        print(potential_lab_owner_row)
        print(potential_lab_owner_row["u_subnet"])

        try:
            # ip_addr is a class.
            ip_addr = IPAddress(ip_address)  #tells you the ip range and does the calculations
            if "u_subnet" in potential_lab_owner_row and potential_lab_owner_row["u_subnet"]:
                subnet = IPNetwork(potential_lab_owner_row["u_subnet"])

                if ip_addr in subnet:
                    return potential_lab_owner_row
                else:
                    print("{0} is not in subnet {1}".format(ip_address, potential_lab_owner_row["u_subnet"]))
                    continue
            else:
                print('no u_subnet key in potential_lab_owner_row or blank')

        except Exception as e:
            print("ERR: {0}".format(potential_lab_owner_row))

    # If IP address was not in any owner subnets, return None
    return None