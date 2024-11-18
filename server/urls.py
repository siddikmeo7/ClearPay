from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include("django.contrib.auth.urls")), # For Authentication
    path('accounts/',include('accounts.urls')), # Defining our Accounts Application
    path('clearpay/',include('ClearPay.urls')), # ClearPay Application
    
]
