from django.urls import path

from users.api import CreateUserView

urlpatterns = [
    path('', CreateUserView.as_view())
]
