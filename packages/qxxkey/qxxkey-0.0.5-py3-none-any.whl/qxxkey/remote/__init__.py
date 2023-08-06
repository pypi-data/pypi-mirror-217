import webbrowser
import requests

def get_authorization_code():
    # URL for Google OAuth2 authorization
    auth_url = "https://accounts.google.com/o/oauth2/auth"
    
    # Parameters for the authorization request
    params = {
        "client_id": "618961871174-n04h46k7mumlhdp6a0uvhqett8n80iel.apps.googleusercontent.com",
        "redirect_uri": "https://qxxkey-e548d.firebaseapp.com/__/auth/handler",
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/userinfo.email",
    }
    
    # Construct the authorization URL
    auth_url += "?" + "&".join(f"{key}={value}" for key, value in params.items())
    
    # Open the authorization URL in a web browser window
    webbrowser.open(auth_url)
    
    # Wait for the user to authorize the application manually
    # and obtain the authorization code
    
    authorization_code = input("Enter the authorization code: ")
    
    return authorization_code

# Call the function to get the authorization code
authorization_code = "4/0AZEOvhUqm-fPXeCUPcOcMKcI8YQp-DE9pF-kkijQtEQSDo7g5lxp2Nj5fn4MyEwRrnGgwQ"
access_token = validate_code(authorization_code)
print(authorization_code)
print(access_token)

# You can now use the authorization code to obtain the access token
# and perform authenticated requests to the Google API
