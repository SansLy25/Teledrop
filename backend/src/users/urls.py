from django.urls import path

from users import views

urlpatterns = [path("profile", views.UserProfileView.as_view())]
