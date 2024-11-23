
from django.views.generic import TemplateView
from django.urls import path, include
from . import views


urlpatterns = [
    # path('', views.home, name='home'),
    path('', TemplateView.as_view(template_name='core/index.html'), name='home'),
]
