from django.conf.urls import url
from camada import views

urlpatterns = [
    url(r'^cadlocal/$', views.local),
]
