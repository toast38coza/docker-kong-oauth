from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.http import HttpResponseRedirect
from oauth import kong

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
    return render(request, 'oauth.html', context)


@require_http_methods(["POST"])
def perform_oauth(request):

    client_id = request.POST.get('client_id')
    user_id = request.POST.get('user_id')
    response = kong.get_access_code(client_id, user_id)

    print (response.content)

    redirect_url = response.json().get('redirect_uri')
    return HttpResponseRedirect(redirect_url)
