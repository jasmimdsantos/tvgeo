from django.conf.urls import url
from impacto import views



urlpatterns = [

    url(r'^quadro/', views.quadro),

    url(r'^api/get_empresas', views.api_get_empresas),
    url(r'^lst_empresa/$', views.lst_empresas),

    url(r'^api/get_projetos/(?P<empresas>\d+)/$', views.api_get_projetos),
    url(r'^lst_projetos/$', views.lst_projetos),

    url(r'^perfil_projeto/(?P<projeto>\d+)/$', views.perfil_projeto),

    url(r'^create_area/(?P<projeto>\d+)/$', views.create_area),
    url(r'^create_impacto/(?P<projeto>\d+)/(?P<faseprojeto>\d+)/$', views.create_impacto),
    url(r'^create_diagnostico/(?P<projeto>\d+)/(?P<faseprojeto>\d+)/$', views.create_diagnostico),

    url(r'^area/(?P<area>\d+)/$', views.view_area),
    url(r'^impacto/(?P<impacto>\d+)/$', views.view_impacto),

    url(r'^$', views.impacto),

]
