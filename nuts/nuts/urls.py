"""nuts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import nuts_app.views

urlpatterns = [
    # bw
    url(r'^admin/', admin.site.urls),
    url(r'^nuts/', include('nuts_app.urls')),
    # url(r'^$', nuts_app.views.display_view.display_home, name='display_home'),
    # bw : welcome
    url(r'^$', nuts_app.views.account_manage_view.display_welcome, name='display_welcome'),

    # bw: for default image
    url(r'^media/', nuts_app.views.profile_view.get_default_photo),
]
