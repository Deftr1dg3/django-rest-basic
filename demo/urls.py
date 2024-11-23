from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('transaction/', views.transaction_example, name='transaction'),
    path('email/', views.send_email, name='send_email'),
    path('task/', views.background_task, name='execute_background_task'),
    path('caching/', views.Demo.as_view(), name='caching_example'),
    path('logging/', views.LoggingView.as_view(), name='logging_view')
]
