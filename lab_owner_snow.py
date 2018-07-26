import pysnow
import json
import os
import csv
import nexpose
from netaddr import *


#Variables


# Takes care of refreshing the token storage if needed
def updater(new_token):
    print("OAuth token refreshed!")
    store['token'] = new_token

    if os.path.exists('token'):
        with open('token', 'r') as f:
            store['token'] = json.load(f)

    else:
        # No previous token exists. Generate new.
        username = raw_input("Enter Username: ")
        word_of_pass = raw_input("Enter Password: ")
        store['token'] = client.generate_token(username, word_of_pass)
        print (store['token'])
        with open('token', 'w') as f:
            f.write(json.dumps(store['token']))

def get_snow_client():
        # Create the OAuthClient with the ServiceNow provided `client_id` and `client_secret`, and a `token_updater`
        # function which takes care of refreshing local token storage.
    client = pysnow.OAuthClient(client_id=client_ID, client_secret=word_of_pass,
                                token_updater=updater, instance=instance)

    # Set the access / refresh tokens
    client.set_token(store['token'])

    return client


def get_lab_owner_by_ip(ip_address):
    global client
    if not client:
        client = get_snow_client()

    class_c_address = ".".join(ip_address.split(".")[0:3])

    # We should now be good to go. Let's define a `Resource` for the incident API.
    lab_owner_resource = client.resource(api_path='/table/u_lab_owners')

    # Query incident records
    qb = (
        pysnow.QueryBuilder()
            .field('u_ip_address').contains(class_c_address)
    )
    potential_lab_owner_rows = lab_owner_resource.get(query=qb)

    # Check all (filtered) lab owner ranges for IP address
    for potential_lab_owner_row in potential_lab_owner_rows:
        if IPAddress(ip_address) in IPNetwork(potential_lab_owner_row["u_ip_subnet"]):
            return potential_lab_owner_row

    # If IP address was not in any owner subnets, return None
    return None