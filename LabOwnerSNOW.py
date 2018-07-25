import pysnow
import json
import os
import csv
import nexpose
#Uploading data into a table in SNOW

#Variables
client_ID = '<insert client id here>'
instance = '<insert instance name>'
word_of_pass= '<insert field>'
store = {'token': None}


# Takes care of refreshing the token storage if needed
def updater(new_token):
    print("OAuth token refreshed!")
    store['token'] = new_token

# Create the OAuthClient with the ServiceNow provided `client_id` and `client_secret`, and a `token_updater`
# function which takes care of refreshing local token storage.
client = pysnow.OAuthClient(client_id=client_ID, client_secret=word_of_pass,
                            token_updater=updater, instance=instance)

if os.path.exists('token'):
    with open ('token', 'r') as f:
        store['token'] = json.load(f)

else:
    # No previous token exists. Generate new.
    username = raw_input("Enter Username: ")
    word_of_pass = raw_input("Enter Password: ")
    store['token'] = client.generate_token(username, word_of_pass)
    print (store['token'])
    with open('token', 'w') as f:
        f.write(json.dumps(store['token']))

# Set the access / refresh tokens
client.set_token(store['token'])

# We should now be good to go. Let's define a `Resource` for the incident API.
lab_owner_resource = client.resource(api_path='/table/<table name>')
with open('<insert file location>','r') as f:
    reader= csv.DictReader(f)
    for row in reader:
        lab_row = {}
        for key, value in row.items():
            lab_row['u_' + key.lower().replace(' ', '_')] = value
        lab_owner_resource.create(lab_row)