from django.urls import path

from storage import views


urlpatterns = [
    path("folders/root", views.RootRetrieveView.as_view()),
    path("folders/<int:id>", views.FolderView.as_view()),
    # path('files/<int:id>'),
    # path('files/<int:id>/download')
]
