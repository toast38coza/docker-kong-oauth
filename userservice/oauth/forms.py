from django import forms
from oauth import kong 

class ClientApplicationForm(forms.Form):
    
    application_name = forms.CharField(label='Application name', max_length=100)
    redirect_uri = forms.CharField(label='Redirect', max_length=100)

    def save(self, consumer_id):

    	data = self.cleaned_data

    	app_name = data.get("application_name")
    	redirect_uri = data.get("redirect_uri")
    	return kong.create_client_application(consumer_id, app_name, redirect_uri)

