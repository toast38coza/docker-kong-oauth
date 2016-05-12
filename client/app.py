from flask import Flask, render_template, request
import requests, os

app = Flask(__name__)

## settings:
client_id = os.environ.get('client_id', None)
client_secret = os.environ.get('client_secret', None)

@app.route("/")
def hello():

    code = request.args.get('code', None)

    if code is not None:
        # get token
        return requests.post(url, data, headers=headers, verify=False)

        # call service 1
        # call service 2

    context = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
    }
    return render_template('index.html', **context)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

"""
curl http://docker.local:8000/oauth2/token \
     -H "Host: service1.com" \
     -H "x-forwarded-proto: https" -d "grant_type=authorization_code" -d "client_id=b4b123e18f3349e6bc7172a656692612" -d "client_secret=10639ab4622147318f7910bcf7b7b460"  -d "code=b1485adbf74745e8b39bf53b0fd76118" --insecure  
"""    