"""rxdashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

from dashboard import views
from dashboard.views import date_form, index, summary_page, calculation_page, dashboard
from django.conf.urls import url
#from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('date/', date_form),
    path('', index),
    path('summary/', summary_page),
    path('calculations/', calculation_page),
    path('dashboard/', dashboard),
    url('signup/', views.SignUpView.as_view(), name='signup'),
    url('validate_username/', views.validate_username, name='validate_username')
              ] +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
