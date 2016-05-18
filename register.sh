curl -X POST \
  --url http://$1:8001/apis/ \
  --data "name=service1" \
  --data "upstream_url=http://$1:8003" \
  --data "request_host=service1.com" \
  --data "request_path=/service1" \
  --data "strip_request_path=true" 

curl -X POST \
  --url http://$1:8001/apis/ \
  --data "name=service2" \
  --data "upstream_url=http://$1:8004" \
  --data "request_host=service2.com" \
  --data "request_path=/service2" \
  --data "strip_request_path=true"   
