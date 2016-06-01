from django.conf.urls import url
from impacto import views



urlpatterns = [
    url(r'^quadro/', views.quadro),
]
