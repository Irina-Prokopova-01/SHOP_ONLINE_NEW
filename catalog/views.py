from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from .models import Product, Category
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ProductForm
from .service import category_products, get_product_list
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    View,
)


class CategoryListView(ListView):
    """Контроллер отображения списка категорий продуктов."""

    model = Category
    template_name = "catalog/category_list.html"


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


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/product_list.html"

    def get_queryset(self):
        return get_product_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["published_products"] = Product.objects.filter(publish_status=True)
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")
    login_url = reverse_lazy("users:login")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if self.request.user != product.owner:
            return HttpResponseForbidden("У вас не достаточно прав.")

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if (
            not self.request.user.has_perm("delete_product")
            or self.request.user != product.owner
        ):
            return HttpResponseForbidden("У вас не достаточно прав.")

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")


class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not request.user.has_perm("can_unpublish_product"):
            return HttpResponseForbidden("У вас не достаточно прав.")

        product.publish_status = False
        product.save()
        return redirect("catalog:product_list")


class CategoryProductView(LoginRequiredMixin, ListView):
    """Контроллер отображения всех продуктов в отдельной категории."""

    template_name = "catalog/category_product.html"
    context_object_name = "products"
    login_url = reverse_lazy("users:login")

    def get_queryset(self):
        print(self.kwargs)
        pk = self.kwargs.get("pk")
        print(pk)
        return category_products(pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.get_queryset()
        return context