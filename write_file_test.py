import dropbox
import json

# Load credentials from creds.json file
with open('creds.json', 'r') as f:
    credentials = json.load(f)

# Create Dropbox object using credentials from json file
try:
    dbx = dropbox.Dropbox(oauth2_access_token=credentials['access_token'], app_key=credentials['app_key'],
                          oauth2_refresh_token=credentials['refresh_token'], app_secret=credentials['app_secret'])
    #dbx = dropbox.Dropbox(oauth2_access_token=credentials['access_token'])
except Exception as e:
    print('Error: ' + e)

# dbx = dropbox.Dropbox(oauth2_access_token=credentials['access_token'], app_key=credentials['app_key'], oauth2_refresh_token=credentials['refresh_token'])
# dbx = dropbox.Dropbox(app_key=credentials['app_key'], oauth2_refresh_token=credentials['refresh_token'])
# dbx = dropbox.Dropbox(oauth2_access_token=credentials['access_token'])

# Get current Dropbox account
print('Current dropbox account:')
print(dbx.users_get_current_account().email)

# Dropbox uploads require binary type, so use 'rb'
with open('C:\\uploadtest.txt', 'rb') as f:
    data = f.read()

# Upload method. '/' represents to root of the Dropbox 'App' folder correlating to the api token above
dbx.files_upload(data, '/uploadtest1.txt')

# Download method. Returns both metadata (md) and a http response from the 'requests' module (res)
with open('C:\\temp\\downloadtest.txt', 'wb') as f:
    md, res = dbx.files_download('/uploadtest1.txt')
    f.write(res.content)

# List all files
print("\nListing all files in folder:")
for entry in dbx.files_list_folder('').entries:
    print(entry.name)

# Delete method. Self explanatory.
dbx.files_delete('/uploadtest1.txt')

# List all files after deletion
print("\nListing all files after deletion:")
for entry in dbx.files_list_folder('').entries:
    print(entry.name)
