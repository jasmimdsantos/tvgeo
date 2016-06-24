from django.conf.urls import url
from camada import views

urlpatterns = [
    url(r'^api/local/lista/$', views.api_lista_local),
    url(r'^local/$', views.lista_local),

    url(r'^api/local/criar_editar/$', views.api_editar_local),
    url(r'^local/criar/$', views.criar_local),
    url(r'^local/editar/(?P<id_local>\d+)/$', views.editar_local),
    url(r'^local/remover/(?P<id_local>\d+)/$', views.remover_local),
    url(r'^local/ver/(?P<id_local>\d+)/$', views.ver_local),




]
