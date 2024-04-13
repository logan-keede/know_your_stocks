"""
URL configuration for know_your_stocks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sites.models import Site
import sys
from allauth.socialaccount.models import SocialApp
import os
from django.urls import path, include
import stocks  
if ('runserver' in sys.argv) or ("TnPplatform.wsgi:application" in sys.argv):
    # if not Student.objects.filter(username=os.getenv("username")).exists():
        # Student.objects.create_superuser(username=os.getenv("username"),email=os.getenv("email"), password=os.getenv("password"))
    if not Site.objects.filter(domain="127.0.0.1:8000").exists():
        Site.objects.create(name="127.0.0.1:8000", domain="127.0.0.1:8000")
    if not SocialApp.objects.filter(provider="google").exists():
        SocialApp.objects.create(provider="google", name="Google", client_id=os.getenv("client"), secret=os.getenv("secret")).sites.set(Site.objects.filter(domain="127.0.0.1:8000"))
urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    path("stocks/", include('stocks.urls'))
]
