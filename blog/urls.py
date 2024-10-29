from django.urls import path
from blog.apps import BlogConfig
from blog.views import (
    PostListView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    PostCreateView,
    ContactsView,
)


app_name = BlogConfig.name

urlpatterns = [
    path("blogs", PostListView.as_view(), name="post_list"),
    path("blogs/contacts/", ContactsView.as_view(), name="contacts"),
    path("blogs/post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("blogs/post/create", PostCreateView.as_view(), name="post_create"),
    path("blogs/post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("blogs/post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
]
