# docker-kong-oauth
An example of implementing Kong's oauth plugin with docker

**Warning:** Work in Progress

**Progress**

* [x] MicroService's with docker-compose
* [x] Manually register all services + verify how OAuth plugin functions
* [.] Create actual authentication backend which interacts with Kong OAuth using Django's user management system
* [.] Automate initial API registration etc via shell script / python script / go script. 
* [.] [Profit](http://www.lstreetc.com/wp-content/uploads/2014/04/Underpants-Gnomes.png)
* [.] Write linked blog post



**Questions**

1. **Q:** If I get an access token for a downstream API, is it useable on other downstream APIs? <br/>
**A:** Yes
1. ...