from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)


class ContactsView(TemplateView):
    template_name = "blog/contacts.html"

    def contacts(self, request, *args, **kwargs):
        """Обрабатываем форму и возвращаем ответ"""
        if self.request.method == "POST":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            message = request.POST.get("message")
            return HttpResponse(
                f"Спасибо, {name}, за Ваше сообщение! Наши специалисты скоро свяжутся с Вами по номеру телефона {phone}!"
            )
        return render(request, "contacts.html")


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(publication_sign=True)


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    # fields = ("title", "text", "image", "publication_sign")
    success_url = reverse_lazy("blog:post_list")


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    # fields = ("title", "text", "image", "publication_sign")
    success_url = reverse_lazy("blog:post_list")

    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    fields = ("title", "text", "image", "publication_sign")
    success_url = reverse_lazy("blog:post_list")
