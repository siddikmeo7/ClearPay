from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('',HomeView.as_view(),name='Base-Page'),
    # User
    path('profileuser/<int:pk>',DetailUserView.as_view(),name='Detail-User'),
    # Client
    path('clients',ClientListView.as_view(),name='Client-List'),
    path('clientdetail/<int:pk>',ClientDetailView.as_view(),name='Client-Detail'),
    path('addclient/',CreateClientView.as_view(), name='Add-Client'),
    path('editclient/<int:pk>',UpdateClientView.as_view(),name='Update-Client'),
    path('deleteclient/<int:pk>',DeleteClientView.as_view(),name='Delete-Client'),
    # Transaction
    path('transactions/create/<int:client_id>/', CreateTransactionView.as_view(), name='Create-Transaction'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
