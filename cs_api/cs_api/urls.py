from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

from api import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts", views.accounts_view, name="accounts_view"),
    path("api/accounts/<int:id>", views.user_delete, name="user_delete"),
    path("api/auth/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/transactions", views.create_transaction, name="create_transaction"),
]
