curl -X POST http://docker.local:8001/apis/$1/plugins \
    --data "name=oauth2" 
curl -X POST http://docker.local:8001/apis/$2/plugins \
    --data "name=oauth2" 
