from django.urls import path
from . import views

urlpatterns = [
    path("", views.apiOverview, name="api-overview"),
    path("bucket-list/", views.bucketList, name="bucket-list"),
    path("bucket-create/", views.bucketCreate, name="bucket-create"),
    path("bucket-update/<str:pk>/", views.bucketUpdate, name="bucket-update"),
    path("bucket-delete/<str:pk>/", views.bucketDelete, name="bucket-delete"),
    path("bucket/<str:bucket_pk>/tasks", views.bucketTasks, name="bucket-tasks"),
    path("bucket/<str:bucket_pk>/task-create/", views.taskCreate, name="task-create"),
    path(
        "bucket/<str:bucket_pk>/task-update/<str:pk>/",
        views.taskUpdate,
        name="task-update",
    ),
    path(
        "bucket/<str:bucket_pk>/task-delete/<str:pk>/",
        views.taskDelete,
        name="task-delete",
    ),
]
