from django.urls import path
from . import views
from .views import ClientList, Client_DetApi

app_name = 'clients'

urlpatterns = [
    path("", views.clients_list, name="list"),
    path("<int:pk>/", views.clients_detail, name="detail"),
    path("<int:pk>/delete/", views.clients_delete, name="delete"),
    path("<int:pk>/edit/", views.clients_edit, name="edit"),
    path("<int:pk>/add-comment/", views.clients_detail, name="add_comment"),
    path("<int:pk>/add-file/", views.clients_add_file, name='add_file'),
    path("add/", views.clients_add, name="add"),
    path('export/', views.clients_export, name='export'),
    
    path('api/', ClientList.as_view(), name='api'),
    path('detapi/<int:pk>', Client_DetApi.as_view(), name='detapi'),
]
