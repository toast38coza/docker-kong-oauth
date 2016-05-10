curl -i -X POST \
  --url http://docker.local:8001/apis/ \
  --data 'name=service1' \
  --data 'upstream_url=http://docker.local:8003/' \
  --data 'request_host=service1.com' \
  --data 'request_path=/service1' \
  --data 'strip_request_path=true' 

curl -i -X POST \
  --url http://docker.local:8001/apis/ \
  --data 'name=service2' \
  --data 'upstream_url=http://docker.local:8004' \
  --data 'request_host=service2.com' \
  --data 'request_path=/service2' \
  --data 'strip_request_path=true'   

curl -X POST http://docker.local:8001/apis/baa777ec-ae40-46f3-98eb-e4ee00474743/plugins \
    --data "name=oauth2"  

{"api_id":"baa777ec-ae40-46f3-98eb-e4ee00474743","id":"e80d4743-26b5-4846-8dce-fbb0e393766c","created_at":1462821458000,"enabled":true,"name":"oauth2","config":{"mandatory_scope":false,"token_expiration":7200,"enable_implicit_grant":false,"hide_credentials":false,"provision_key":"c776b1cdd4974e85a7fc8e1390ce7769","accept_http_if_already_terminated":false,"enable_authorization_code":true,"enable_client_credentials":false,"enable_password_grant":false}}

curl -X POST http://docker.local:8001/apis/8832a1f2-a427-4ba8-bee8-e34fa894d682/plugins \
    --data "name=oauth2"  
{"api_id":"8832a1f2-a427-4ba8-bee8-e34fa894d682","id":"3e039cc5-fe59-49c6-a804-f69631b5fc96","created_at":1462821497000,"enabled":true,"name":"oauth2","config":{"mandatory_scope":false,"token_expiration":7200,"enable_implicit_grant":false,"hide_credentials":false,"provision_key":"7656a7f4dee345a6a1270a273c099480","accept_http_if_already_terminated":false,"enable_authorization_code":true,"enable_client_credentials":false,"enable_password_grant":false}}    

curl -X POST http://docker.local:8001/consumers/ \
    --data "username=user123" \
    --data "custom_id=1"

{"custom_id":"1","username":"user123","created_at":1462821574000,"id":"26550d58-68f0-4f25-8ab0-4174998474e6"}

curl -X POST http://docker.local:8001/consumers/26550d58-68f0-4f25-8ab0-4174998474e6/oauth2 \
    --data "name=Test%20Application" \
    --data "redirect_uri=http://docker.local/login-redirect/"      

{"consumer_id":"26550d58-68f0-4f25-8ab0-4174998474e6","client_id":"b4b123e18f3349e6bc7172a656692612","id":"7b196bc0-531b-47d9-a48c-bd605bdb949c","redirect_uri":"http:\/\/docker.local\/login-redirect\/","name":"Test Application","created_at":1462821732000,"client_secret":"10639ab4622147318f7910bcf7b7b460"}    

# get code:
curl http://docker.local:8000/oauth2/authorize \
    --header "Host: service1.com" \
    --header "x-forwarded-proto: https" \
    --data "client_id=b4b123e18f3349e6bc7172a656692612" --data "response_type=code" --data "provision_key=7656a7f4dee345a6a1270a273c099480" --data "authenticated_userid=user123"

curl http://docker.local:8000/oauth2/authorize \
    --header "Host: service1.com" \
    --header "x-forwarded-proto: https" \
    --data "client_id=b4b123e18f3349e6bc7172a656692612" --data "response_type=code" --data "provision_key=7656a7f4dee345a6a1270a273c099480" --data "authenticated_userid=user123"


curl https://192.168.99.100:8443/oauth2/authorize \
    --header "Host: service1.com" \
    --data "client_id=b4b123e18f3349e6bc7172a656692612" --data "response_type=code" --data "provision_key=7656a7f4dee345a6a1270a273c099480" --data "authenticated_userid=user123" --insecure



# swap code for token:
curl http://docker.local:8000/oauth2/token \
     -H "Host: service1.com" \
     -H "x-forwarded-proto: https" -d "grant_type=authorization_code" -d "client_id=b4b123e18f3349e6bc7172a656692612" -d "client_secret=10639ab4622147318f7910bcf7b7b460"  -d "code=b1485adbf74745e8b39bf53b0fd76118" --insecure  

{"refresh_token":"eb0b6bcc3f324355a48330bc1d7282cc","token_type":"bearer","access_token":"1dff90f960b342a488ef67d791e15b22","expires_in":7200}

curl -i -X GET \
  --url http://docker.local:8000?access_token=1dff90f960b342a488ef67d791e15b22 \
  --header 'Host: service1.com' 

curl -i -X GET \
  --url http://docker.local:8000?access_token=1dff90f960b342a488ef67d791e15b22 \
  --header 'Host: service2.com' 


