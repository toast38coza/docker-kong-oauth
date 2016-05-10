from django.conf import settings
from django.contrib.auth.models import User
import requests

def get_consumer(consumer_id):	
	url = "{}/consumers/{}" . format (settings.KONG_ADMIN_URL, consumer_id)
	return requests.get(url) 

def get_client(client_id):
	url = "{}/oauth2?client_id={}" . format (settings.KONG_ADMIN_URL, client_id)
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