"""
URL configuration for devangwa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import index

urlpatterns = [
    # re_path(r'^.*$', index, name='index'),
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/', include('course.urls')),
    path('api/v1/coaching/', include('coaching.urls')),
    path('api/v1/community/', include('community.urls')),
    re_path(r'^api/v1/auth/', include('djoser.urls')),
    # re_path(r'^api/v1/auth/', include('djoser.urls.jwt')),
    path('api/v1/auth/jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)