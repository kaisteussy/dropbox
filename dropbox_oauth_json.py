import dropbox
import webbrowser
import json

try:
    with open('creds.json', 'r') as f:
        oauth_creds = json.load(f)
except FileNotFoundError as e:
    print('ERROR: Unable to load credentials\n' + str(e))
    exit()
else:
    print('Opened creds.json...')

app_key = oauth_creds['app_key']
app_secret = oauth_creds['app_secret']


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


# Store the results of the oauth flow
oauth_result = dbx_oauth_flow(app_key, app_secret)

access_token = oauth_result.access_token
refresh_token = oauth_result.refresh_token

oauth_creds['refresh_token'] = refresh_token
oauth_creds['access_token'] = access_token

# Save the refresh token and access token to json file
with open('creds.json', 'w') as f:
    json.dump(oauth_creds, f)
