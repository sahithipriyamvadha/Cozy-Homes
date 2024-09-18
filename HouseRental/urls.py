"""HouseRental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from rental_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('add_user_registration/', views.add_user_registration),
    path('login/', views.login),
    path('logout/', views.logout),
    path('user_registration/', views.user_registration),
    path('login_validation/', views.login_validation),
    path('landlord_home/', views.landlord_home),
    path('tenant_home/', views.tenant_home),
    path('landlord_profile/', views.landlord_profile),
    path('update_landlord_user/', views.update_landlord_user),
    path('tenant_profile/', views.tenant_profile),
    path('update_tenant_user/', views.update_tenant_user),
    path('add_rent_house/', views.add_rent_house),
    path('add_house_details/', views.add_house_details),
    path('house_list/', views.house_list),
    path('delete_house/<int:house_id>/', views.delete_house),
    path('edit_house/<int:house_id>/', views.edit_house, name='edit_house'),
    path('update_house/<int:house_id>/', views.update_house, name='update_house'),
    path('landlord_details/<int:landlord_id>/', views.landlord_details, name='landlord_details'),
    path('admin_home/', views.admin_home),
    path('admin_landlords/', views.admin_landlords),
    path('admin_tenants/', views.admin_tenants),
    path('admin_landlord_houses/', views.admin_landlord_houses),
    
    
]
