from django.conf.urls import url
from impacto import views



urlpatterns = [

    url(r'^quadro/', views.quadro),

    url(r'^api/get_empresas', views.api_get_empresas),
    url(r'^lst_empresa/$', views.lst_empresas),

    url(r'^api/get_projetos/(?P<empresas>\d+)/$', views.api_get_projetos),
    url(r'^projetos/$', views.lst_projetos),

    url(r'^projetos/perfil_projeto/(?P<projeto>\d+)/$', views.perfil_projeto),

    url(r'^projetos/perfil_projeto/criar_area/(?P<projeto>\d+)/$', views.create_area),
    url(r'^projetos/perfil_projeto/criar_impacto_projeto/(?P<projeto>\d+)/(?P<faseprojeto>\d+)/$', views.create_impacto),
    url(r'^projetos/perfil_projeto/criar_diagnostico/(?P<projeto>\d+)/(?P<faseprojeto>\d+)/$', views.create_diagnostico),

    url(r'^projetos/perfil_projeto/ver_impacto/(?P<impacto>\d+)/$', views.view_impacto),

    url(r'^projetos/perfil_projeto/editar_area/(?P<area>\d+)/$', views.edit_area),
    url(r'^projetos/perfil_projeto/editar_impacto_projeto/(?P<impacto>\d+)/$', views.edit_impacto_proj),
    url(r'^projetos/perfil_projeto/editar_diagnostico/(?P<diagnostico>\d+)/$', views.edit_diagnostico),

    url(r'^$', views.impacto),

]
