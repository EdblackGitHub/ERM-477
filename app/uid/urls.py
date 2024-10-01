from django.urls import path
from . import views

app_name = 'uid'

urlpatterns = [
    path('generate-uid/', views.generate_uid_node, name='generate_uid'),
    path('create-provider/', views.create_provider, name='create_provider'),
    path('create-lcvterm/', views.create_lcvterm, name='create_lcvterm'),
    path('success/', views.success_view, name='success'),
]