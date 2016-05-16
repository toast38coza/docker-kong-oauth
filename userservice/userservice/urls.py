"""userservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from oauth import views

urlpatterns = [
    url(r'^oauth/', views.oauth_allow_access, name="oauth"),
    url(r'^authorize/', views.perform_oauth),
    url(r'^application/', views.create_application),
    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
]
