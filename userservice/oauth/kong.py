from django.conf import settings
from django.contrib.auth.models import User
import requests

def create_consumer(user):
    """
    curl -X POST http://docker.local:8001/consumers/ \
    --data "username=user123" \
    --data "custom_id=1"
    """
    data = {
        "username": user.username,
        "custom_id": user.pk
    }
    url = "{}/consumers/" . format (settings.KONG_ADMIN_URL)
    return requests.post(url, data) 

def create_client_application(consumer_id, app_name, redirect_uri):
    """
    curl -X POST http://docker.local:8001/consumers/26550d58-68f0-4f25-8ab0-4174998474e6/oauth2 \
    --data "name=Test%20Application" \
    --data "redirect_uri=http://docker.local"   
    """
    
    data = {
        "name": app_name,
        "redirect_uri": redirect_uri
    }
    url = "{}/consumers/{}/oauth2" . format (settings.KONG_ADMIN_URL, consumer_id)
    return requests.post(url, data)

def get_consumer_clients(consumer_id):
    url = "{}/consumers/{}/oauth2" . format (settings.KONG_ADMIN_URL, consumer_id)
    return requests.get(url)

def get_or_create_consumer(user):
    consumer_response = get_consumer_by_username(user.username)
    if consumer_response.status_code == 404:
        consumer_response = create_consumer(user)
    return consumer_response

def get_consumer(consumer_id):  
    url = "{}/consumers/{}" . format (settings.KONG_ADMIN_URL, consumer_id)
    return requests.get(url) 

def get_consumer_by_username(username):  
    url = "{}/consumers/{}" . format (settings.KONG_ADMIN_URL, username)
    return requests.get(url)     

def get_client(client_id):
    url = "{}/oauth2?client_id={}" . format (settings.KONG_ADMIN_URL, client_id)
    return requests.get(url)
   
def get_plugins(api_id):
    url = "{}/apis/{}/plugins" . format (settings.KONG_ADMIN_URL, api_id)
    return requests.get(url)

def get_plugin(api_id, plugin_id):
    """
    http://docker.local:8001/apis/baa777ec-ae40-46f3-98eb-e4ee00474743/plugins/e80d4743-26b5-4846-8dce-fbb0e393766c
    """ 
    url = "{}/apis/{}/{}" . format (settings.KONG_ADMIN_URL, api_id, plugin_id)
    return requests.get(url)

def get_access_code(client_id, user_id):
    """
    curl http://docker.local:8000/oauth2/authorize \
    --header "Host: service1.com" \
    --header "x-forwarded-proto: https" \
    --data "client_id=b4b123e18f3349e6bc7172a656692612" 
    --data "response_type=code" 
    --data "provision_key=7656a7f4dee345a6a1270a273c099480" 
    --data "authenticated_userid=user123"
    """

    oauth_host = settings.OAUTH_SERVICE.get("host")
    provision_key = settings.OAUTH_SERVICE.get("provision_key")

    url = "{}/oauth2/authorize" . format (settings.KONG_URL)
    headers = { "Host": oauth_host }    
    data = {
        "client_id": client_id,
        "response_type": "code",
        "provision_key": provision_key,
        "authenticated_userid": user_id
    }
    return requests.post(url, data, headers=headers, verify=False)

def get_token(code, client_id, client_secret):
    """
    Given an access code, get the token
    ---
    curl http://docker.local:8000/oauth2/token \
    -d "grant_type=authorization_code" -d "client_id=b4b123e18f3349e6bc7172a656692612" -d "client_secret=10639ab4622147318f7910bcf7b7b460"  -d "code=b1485adbf74745e8b39bf53b0fd76118" --insecure  

    """ 
    oauth_host = settings.OAUTH_SERVICE.get("host")
    headers = { "Host": oauth_host }    
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
    }
    url = "{}/oauth2/token" . format (settings.KONG_URL)
    return requests.post(url, data, headers=headers, verify=False)
