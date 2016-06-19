# docker-kong-oauth
An example of implementing Kong's oauth plugin with docker

> **Warning:** Work in Progress

## Getting Started

```
docker-compose up -d && docker-compose logs
```

This will launch the following (assuming docker-machine ip is: `192.168.99.100`):

* Kong: 192.168.99.100:8000 
* Kong Admin: 192.168.99.100:8001 
* UserService: 192.168.99.100:8002 - this will authenticate our users with OAuth
* Client: 192.168.99.100 - A client which will authenticate via OAuth and make requests to the upstream services
* Service1: 192.168.99.100:8003 - An upstream service
* Service2: 192.168.99.100:8004 - Another upstream service 

* Kong Dashboard: 192.168.99.100:8999 - A dashboard for administrating Kong

### Register our upstream APIs:

To get setup quickly, there are two bash scripts. To register our upstream services, you can run: 

```
sh ./register.sh {host}
```

for example: 

```
sh ./register.sh '192.168.99.100'
```

This will register both our services. It will spit out the json response. To add oauth. Now, take note of the id's and run:

```
sh ./register2.sh {service1.id} {service2.id}
```

for example.:

```
sh ./register2.sh 0d35c547-1311-4343-a567-7ca670d35637 7e9b3d3e-edc7-4c17-81d0-3f2eac91aaaf
```

Take note of the `provision_id` for service1: At the bottom of `userservice/userservice.settings.py`, set the provision id in `OAUTH_SERVICE.provision_key`

You can now explore around the Kong Dashboard app (running on port 8999), and you should see that both our downstream APIs have been added, and that they each have the oauth2 plugin added to them.

### Register a client application

Ok. Next up, we need to register a client application which a user can give authority to access upstream APIs on their behalf.

We're using Django for our backend user authentication. Let's quickly create an admin user in django: 

```
docker-compose run --rm userservice python manage.py createsuperuser
```

Now, let's go to: 192.168.99.100:8002/application

This should ask you to login. Use the user we just created above. 
After you've logged in, you'll be redirected back to the applications page. 

This will automatically create a consumer in Kong for the current logged in user (in Django). 

From this page, you can create a client. 

So, at this point we have the following in our Kong setup: 

* 2x upstream APIs with oauth2 authentication.
* A consumer which is linked to our consumer in our Django backend.
* A client application which is registered against our consumer.

Now we are ready to authenticate our client using oauth2. 

Edit the file `environment.env` set the `client_id` and `client_secret` to match the values associated with the client application you just created.

Once you've done that: 

* log out of the userservice: http://192.168.99.100:8002/logout/
* Restart our client application (to make the environment variables apply):

    ```
    docker-compose stop client
    docker-compose rm -v client
    docker-compose start client        
    ```

Now let's try authenticate. Go to 192.168.99.100

1. Click _authenticate_
2. You're sent to the userservice to authenticate. Because you're logged out, it will ask you to login. You can use the user above to login again. 
3. Now it will ask you to authorize the client app. Click authorize.

You should be redirected back to the client. The client will spit out the response

**Progress**

* [x] MicroService's with docker-compose
* [x] Manually register all services + verify how OAuth plugin functions
* [x] Create actual authentication backend which interacts with Kong OAuth using Django's user management system
* [x] Automate initial API registration etc via shell script / python script / go script. 
* [x] Add the ability to create the OAuth Client Application 
* [x] Add the client part of the puzzle
* [ ] Make it look nice
* [ ] Write linked blog post
* [ ] [Profit](http://www.lstreetc.com/wp-content/uploads/2014/04/Underpants-Gnomes.png)




**Questions**

1. **Q:** If I get an access token for a downstream API, is it useable on other downstream APIs? <br/>
**A:** Yes
1. ...