"""core URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
from django.contrib import admin
from login import views as login
from clima import  urls


urlpatterns = [
    url(r'^home/', login.webhome, name='webhome'),
    url(r'^mudasenha/', login.mudasenha, name="mudasenha"),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', include('login.urls')),
    url(r'^webhome/', include('login.urls')),
    url(r'^accounts/login/', include('login.urls')),
    url(r'^clima/', include('clima.urls')),
    url(r'^firemonitor/' , include ( 'firemonitor.urls' ) ) ,
    url ( r'^monitor/' , include ( 'monitor.urls' ) ) ,
    url(r'^impacto/', include('impacto.urls')),
    url(r'^camada/', include('camada.urls')),
    url(r'^$', login.home, name='home'),



]
