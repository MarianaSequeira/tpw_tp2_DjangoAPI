"""
webproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app import views

urlpatterns = [
    path('authenticate', views.CustomAuthToken.as_view()),
    path('receita', views.get_receita),
    path('addreceita', views.save_receita),
    path('receitas', views.get_receitas),
    path('receitatipo', views.get_receita_tipo),
    path('deletereceita/<int:id>', views.delete_receita),
    path('receitasguardadas', views.get_receitas_guardadas),
    path('receitasutilizador', views.get_receitas_utilizador),
    path('receitastag', views.get_receitas_tag),
    path('tagsreceita', views.get_tags_receita),
    path('comentar', views.comentar_receita),
    path('pesquisar', views.pesquisar),
    path('receitasgostadas', views.receitas_gostadas),
    path('ingredientesreceita', views.ingredientes_receita),
    path('tags', views.tags)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

