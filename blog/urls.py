from django.urls import path

from .views import (
    HomeView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostUpdateView,
    dashboard,
    register,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    path("posts/new/", PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
]

