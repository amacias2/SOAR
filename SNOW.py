import pysnow
import json
import os
import nexpose


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
incident_resource = client.resource(api_path='/table/incident')

critical_vulns = nexpose.generate_report()
critical_vuln = critical_vulns[5]
snow_format = {}
for key, val in critical_vuln.items():
    snow_format['u_'+ key] = val
incident_resource.create(snow_format)

'''# Fetch the first record in the response
records = incident_resource.get(query={'number': 'INC0275511'}, stream=True)
record_dict = records.first()

with open('record', 'w') as f:
    json_string = json.dumps(record_dict, indent=4)
    f.write(json_string)

print (json_string)

for record in records.all():
    print(record)


'''
