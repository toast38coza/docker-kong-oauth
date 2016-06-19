from flask import Flask, render_template, request
import requests, os

app = Flask(__name__)

## settings:
client_id = os.environ.get('client_id', None)
client_secret = os.environ.get('client_secret', None)
kong_url = os.environ.get('kong_url', None)

def get_token(code, client_id, client_secret):
    
    oauth_host = "service1.com"
    headers = { "Host": oauth_host }    
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
    }
    url = "{}/oauth2/token" . format (kong_url)
    return requests.post(url, data, headers=headers, verify=False)

@app.route("/")
def hello():

    code = request.args.get('code', None)
    token = None
    service1_response = None
    service2_response = None
    if code is not None:
        # get token

        token = get_token(code, client_id, client_secret).json()
        print (token)
        url1 = "{}/service1?access_token={}" . format (kong_url, token.get('access_token'))
        url2 = "{}/service2?access_token={}" . format (kong_url, token.get('access_token'))
        service1_response = requests.get(url1, verify=False)
        service2_response = requests.get(url2, verify=False)
        # call service 1
        # call service 2

    context = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "token_response": token,
        "service_response1": service1_response,
        "service_response2": service2_response,

    }
    return render_template('index.html', **context)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

"""
curl http://docker.local:8000/oauth2/token \
     -H "Host: service1.com" \
     -H "x-forwarded-proto: https" -d "grant_type=authorization_code" -d "client_id=b4b123e18f3349e6bc7172a656692612" -d "client_secret=10639ab4622147318f7910bcf7b7b460"  -d "code=b1485adbf74745e8b39bf53b0fd76118" --insecure  

curl -X GET 192.168.99.100:8000/service1?access_token=dd9f9fbe63a749d2b2e10310ce992b14

"""    