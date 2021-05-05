import dropbox
import webbrowser
import json

KEY_FILE = 'creds.json'


def load_credentials():
    # Function to load the app_key and app_secret from key file
    try:
        with open(KEY_FILE, 'r') as f:
            oauth_creds = json.load(f)
    except FileNotFoundError as e:
        print('ERROR: Unable to load credentials\n' + str(e))
        exit()
    else:
        print('Loading creds.json...')
        print('creds.json loaded...')
        return oauth_creds


def dbx_oauth_flow(key, secret):
    # Begin the OAuth flow to gather access token and refresh token
    auth_flow = dropbox.oauth.DropboxOAuth2FlowNoRedirect(consumer_key=key, consumer_secret=secret,
                                                          token_access_type='offline')
    authorize_url = auth_flow.start()
    webbrowser.open(authorize_url)
    print('1.Goto: ' + authorize_url)
    print('2.Click ”Allow” (you might have to log in first).')
    print('3.Copy the authorization code.')
    auth_code = input('Enter the authorization code here: ').strip()
    try:
        oauth_flow_result = auth_flow.finish(auth_code)
        print("OAuth flow successful.")
        return oauth_flow_result
    except Exception as e:
        print('Error: ' + e)


# Load credentials from the json file and store.
oauth_creds = load_credentials()
app_key = oauth_creds['app_key']
app_secret = oauth_creds['app_secret']

# Start the oauth flow and store the results
print('Starting the OAuth flow...')
oauth_result = dbx_oauth_flow(app_key, app_secret)

access_token = oauth_result.access_token
refresh_token = oauth_result.refresh_token

oauth_creds['refresh_token'] = refresh_token
oauth_creds['access_token'] = access_token

# Save the refresh token and access token to json file
with open(KEY_FILE, 'w') as f:
    json.dump(oauth_creds, f)
