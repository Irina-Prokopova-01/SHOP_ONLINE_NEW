from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "text", "created_at", "publication_sign", "view_counter")
    search_fields = ("title", "publication_sign")
    list_filter = ("publication_sign",)


