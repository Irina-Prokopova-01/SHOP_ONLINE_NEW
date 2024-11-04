from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import Product
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
    template_name = "catalog/contacts.html"

    def contacts(self, request):
        """Обрабатываем форму и возвращаем ответ"""
        if self.request.method == "POST":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            message = request.POST.get("message")
            return HttpResponse(
                f"Спасибо, {name}, за Ваше сообщение! Наши специалисты скоро свяжутся с Вами по номеру телефона {phone}!"
            )
        return render(request, "contacts.html")


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(CreateView):
    model = Product
    fields = ("title", "description", "price", "image", "category")
    success_url = reverse_lazy("catalog:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = ("title", "description", "price", "image", "category")
    success_url = reverse_lazy("catalog:product_list")

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")


#
# def product_list(request: HttpRequest):
#     """функция обрабатывает запрос и возвращает html-страницу"""
#     if request.method == "GET":
#         products = Product.objects.all()
#         context = {"products": products}
#
#         return render(request, "product_list.html", context=context)
#

# def contacts(request):
#     """Обрабатываем форму и возвращаем ответ"""
#     if request.method == "POST":
#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         message = request.POST.get("message")
#         return HttpResponse(
#             f"Спасибо, {name}, за Ваше сообщение! Наши специалисты скоро свяжутся с Вами по номеру телефона {phone}!"
#         )
#     return render(request, "contacts.html")


# def product_detail(request, pk: int):
#     product = get_object_or_404(Product, pk=pk)
#     context = {"product": product}
#     return render(request, "product_detail.html", context=context)
