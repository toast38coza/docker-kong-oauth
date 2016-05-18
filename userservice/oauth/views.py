from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.http import HttpResponseRedirect
from oauth import kong, forms

@login_required
@require_http_methods(["GET"])
def oauth_allow_access(request):
    
    client_id = request.GET.get('client_id')
    client = kong.get_client(client_id)
    client_data = client.json().get('data')[0]

    consumer_id = client_data.get('consumer_id')
    consumer = kong.get_consumer(consumer_id)

    context = {
        "client": client_data.get("name"),
        "client_id": client_id,
        "consumer": consumer.json().get("username"),
        "user": request.user,
    }
    return render(request, 'oauth/oauth.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def create_application(request):
    
    consumer = kong.get_or_create_consumer(request.user)
    
    if request.method == 'POST':
        application_form = forms.ClientApplicationForm(request.POST)
        if application_form.is_valid():            
            application_form.save(request.user)
    else:
        data = {
            "username": request.user.username,
            "custom_id": request.user.pk,
            "consumer": consumer,
        }
        application_form = forms.ClientApplicationForm(initial=data)

    if consumer is not None:
        client_list = kong.get_consumer_clients(consumer.json().get("id"))


    context = {
        "application_form": application_form,
        "consumer": consumer.json(),
        "client_list": client_list.json()
    }
    return render(request, 'oauth/applications.html', context)

@require_http_methods(["POST"])
def perform_oauth(request):

    client_id = request.POST.get('client_id')
    user_id = request.POST.get('user_id')
    response = kong.get_access_code(client_id, user_id)

    print (response.content)

    redirect_url = response.json().get('redirect_uri')
    return HttpResponseRedirect(redirect_url)
