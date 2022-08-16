"""Authentication_system URL Configuration

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




from django.urls import path
from App import views

# --------- Jwt -------
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView

)



urlpatterns = [
    path('',views.auth_system_func,name='register'),
    path('login',views.login_user,name="login"),
    path('home',views.home_page,name='home'),
    path('Verify/<auth_token>',views.Verify_email),
    path('logout',views.logout_session,name='logout'),
    path('ll',views.serializer_login),

    # --------- Jwt token --------
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # ------ New end point --------
    path('ss',views.func.as_view()),
]
