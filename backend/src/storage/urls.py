from django.urls import path

from storage import views


urlpatterns = [
    path("folders/root", views.RootRetrieveView.as_view()),
    path("folders/<int:id>", views.FolderView.as_view()),
    path("folders/current", views.CurrentFolderView.as_view()),
    path("files/<int:id>", views.FileView.as_view()),
    path("files/<int:id>/move", views.FileMoveView.as_view()),
    path("folders/<int:id>/move", views.FolderMoveView.as_view())
    # path('files/<int:id>/download')
]
