from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Configuration variables
mail_enabled = os.environ.get("MAIL_ENABLED", default="true")
app.config['CLIENT_ID'] = ''
app.config['CLIENT_SECRET'] = ''
app.config['CALLBACK_URL'] = 'http://localhost:8080/api/auth/callback'
app.config['SCOPES'] = 'data:read viewables:read'

@app.route('/')
def redirect():
    return redirect(f"https://developer.api.autodesk.com/authentication/v2/authorize?response_type=code&client_id={app.config['CLIENT_ID']}&redirect_uri={app.config['CALLBACK_URL']}&scope={app.config['SCOPES']}")

@app.route('/api/auth/callback', methods=['POST','GET'])
def callback():
  # Get credential code
  code = request.args.get('code')
  tokenUrl = "https://developer.api.autodesk.com/authentication/v2/token"
  payload = f"grant_type=authorization_code&code={code}&client_id={app.config['CLIENT_ID']}&client_secret={app.config['CLIENT_SECRET']}&redirect_uri={app.config['CALLBACK_URL']}"
  headers = {
      "Content-Type": "application/x-www-form-urlencoded"
  }
  resp = requests.request("POST", tokenUrl, data=payload, headers=headers)
  respJson = resp.json()
  # Return success response
  return f"{respJson}", 200

if __name__ == '__main__':
  app.run(debug=True, port=8080)