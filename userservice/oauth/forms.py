from django import forms
from oauth import kong 

class ClientApplicationForm(forms.Form):
    
    application_name = forms.CharField(label='Application name', max_length=100)
    redirect_uri = forms.CharField(label='Redirect', max_length=100)

    def save(self, user):

    	data = self.cleaned_data
    	consumer_response = kong.create_consumer(user)

    	consumer_id = consumer_response.json().get("id")
    	app_name = data.get("application_name")
    	redirect_uri = data.get("redirect_uri")
    	client_response = kong.create_client_application(consumer_id, app_name, redirect_uri)

    	print (consumer_response.json())
    	print (client_response.json())

    	return (consumer_response.json(), client_response.json())

