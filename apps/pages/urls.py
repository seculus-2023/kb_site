from django.urls import path 
from pages import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'), 
    path('contato', views.contato, name='contato'),
    path('projetos', views.projetos, name='projetos'),
    path('sistemas', views.sistemas, name='sistemas'),
    path('equipe', views.equipe, name='equipe'),
    path('membros', views.membros, name='membros'),
    path('valores', views.valores, name='valores'),
    path('politica', views.politica, name='politica'),
    path('historia', views.historia, name='historia'),
    path('agro', views.agro, name='agro'),
    path('bolsatrader', views.bolsatrader, name='bolsatrader'),
    path('seletivo', views.seletivo, name='seletivo'),
    path('alvara', views.alvara, name='alvara'),

    # PWA: o service worker e a tela offline ficam na raiz do site
    path('sw.js', views.service_worker, name='service_worker'),
    path('offline/', views.offline, name='offline'),
    path('instalar', views.instalar_app, name='instalar_app'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=getattr(settings, 'STATIC_ROOT', 'static'))
