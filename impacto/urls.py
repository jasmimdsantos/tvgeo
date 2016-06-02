from django.conf.urls import url
from impacto import views



urlpatterns = [

    url(r'^quadro/', views.quadro),

    url(r'^api/get_empresas', views.api_get_empresas),
    url(r'^lst_empresa/$', views.lst_empresas),

    url(r'^api/get_projetos/(?P<empresas>\d+)/$', views.api_get_projetos),
    url(r'^lst_projetos/$', views.lst_projetos),

    url(r'^api/get_faseprojeto', views.api_get_faseprojeto),
    url(r'^lst_faseprojeto/$', views.lst_faseprojeto),

    url(r'^perfil_projeto/(?P<projeto>\d+)/$$', views.perfil_projeto),

    url(r'^$', views.impacto),

]
