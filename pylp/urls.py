"""pylp URL Configuration

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
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from content.views import (
    ContactUsView,
    DirectoryView,
    HomeView,
    ResourceListView,
    ResourceView,
    SubmitResourceView,
)
admin.site.site_header = 'ACCESS-PYLP Site Admin'
admin.site.site_title = 'Admin: ACCESS-PYLP'

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('', include('account.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contact-us/', ContactUsView.as_view(), name="contact-us"),
    path('news/', include('news.urls')),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('djrichtextfield/', include('djrichtextfield.urls')),
    path('resources/', ResourceListView.as_view(), name="resource_list"),
    path('resources-add/', SubmitResourceView.as_view(), name="submit-resource"),
    path('resources/<slug:slug>', ResourceView.as_view(), name="resource"),
    path('directory/', DirectoryView.as_view(), name="directory"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
