from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from django.db.models import F

from adminapp.forms import ShopUserAdminCreateForm, ShopUserAdminUpdateForm, CategoriesAdminUpdateForm, \
    ProductAdminUpdateForm
from authapp.models import ShopUser
from mainapp.models import Categories, Products


# Create your views here.

# @user_passes_test(lambda x: x.is_superuser)
# def index(request):
#     object_list = ShopUser.objects.all()
#     content = {
#         'title': 'админка/пользователи',
#         'object_list': object_list,
#     }
#     return render(request, 'adminapp/index.html', content)

class ShopUserListView(ListView):
    model = ShopUser

    # template_name = 'adminapp/index.html'

    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@user_passes_test(lambda x: x.is_superuser)
def shopuser_create(request):
    if request.method == 'POST':
        form = ShopUserAdminCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # приводит к сохранению в базу данных
            return HttpResponseRedirect(reverse('myadmin:index'))
    else:
        form = ShopUserAdminCreateForm()

    content = {
        'title': 'админка/новый пользователь',
        'form': form,
    }

    return render(request, 'adminapp/shopuser_update.html', content)


@user_passes_test(lambda x: x.is_superuser)
def shopuser_update(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        form = ShopUserAdminUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()  # приводит к сохранению в базу данных
            return HttpResponseRedirect(reverse('myadmin:index'))
    else:
        form = ShopUserAdminUpdateForm(instance=user)

    content = {
        'title': 'админка/редактирование пользователя',
        'form': form,
    }

    return render(request, 'adminapp/shopuser_update.html', content)


@user_passes_test(lambda x: x.is_superuser)
def shopuser_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('myadmin:index'))
    elif request.method == 'GET':
        content = {
            'title': 'админка/удаление пользователя',
            'object': user,
        }
        return render(request, 'adminapp/shopuser_delete.html', content)


@user_passes_test(lambda x: x.is_superuser)
def productcategory_list(request):
    object_list = Categories.objects.all()
    content = {
        'title': 'админка/категории',
        'object_list': object_list
    }
    return render(request, 'adminapp/productcategory_list.html', content)


# @user_passes_test(lambda x: x.is_superuser)
# def productcategory_create(request):
#     if request.method == 'POST':
#         form = CategoriesAdminUpdateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()  # приводит к сохранению в базу данных
#             return HttpResponseRedirect(reverse('myadmin:productcategory_list'))
#     else:
#         form = CategoriesAdminUpdateForm()
#
#     content = {
#         'title': 'админка/новая категория',
#         'form': form,
#     }
#
#     return render(request, 'adminapp/productcategory_update.html', content)


class ProductCategoryCreateView(CreateView):
    model = Categories
    # template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('myadmin:productcategory_list')
    # fields = '__all__'
    form_class = CategoriesAdminUpdateForm


# @user_passes_test(lambda x: x.is_superuser)
# def productcategory_update(request, pk):
#     productcategory = get_object_or_404(Categories, pk=pk)
#     if request.method == 'POST':
#         form = CategoriesAdminUpdateForm(request.POST, request.FILES, instance=productcategory)
#         if form.is_valid():
#             form.save()  # приводит к сохранению в базу данных
#             return HttpResponseRedirect(reverse('myadmin:productcategory_list'))
#     else:
#         form = CategoriesAdminUpdateForm(instance=productcategory)
#
#     content = {
#         'title': 'админка/новая категория',
#         'form': form,
#     }
#
#     return render(request, 'adminapp/productcategory_update.html', content)


class ProductCategoryUpdateView(UpdateView):
    model = Categories
    # template_name = 'adminapp/productcategory_list.html'
    success_url = reverse_lazy('myadmin:productcategory_list')
    form_class = CategoriesAdminUpdateForm

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'админка / редактирование категории'
        return content

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.products_set.update(price_product=F('price_product') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        return super().form_valid(form)


# @user_passes_test(lambda x: x.is_superuser)
# def productcategory_delete(request, pk):
#     productcategory = get_object_or_404(Categories, pk=pk)
#     if request.method == 'POST':
#         productcategory.is_active = False
#         productcategory.save()
#         return HttpResponseRedirect(reverse('myadmin:productcategory_list'))
#     elif request.method == 'GET':
#         content = {
#             'title': 'админка/удаление категории',
#             'object': productcategory,
#         }
#         return render(request, 'adminapp/productcategory_delete.html', content)

class ProductCategoryDeleteView(DeleteView):
    model = Categories
    success_url = reverse_lazy('myadmin:productcategory_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda x: x.is_superuser)
def productcategory_products(request, pk):
    productcategory = get_object_or_404(Categories, pk=pk)
    content = {
        'title': 'админка/товары категории',
        'productcategory': productcategory,
        'object_list': productcategory.products_set.all(),
    }

    return render(request, 'adminapp/product_list.html', content)


# @user_passes_test(lambda x: x.is_superuser)
# def product_create(request, pk):
#     productcategory = get_object_or_404(Categories, pk=pk)
#     if request.method == 'POST':
#         form = ProductAdminUpdateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()  # приводит к сохранению в базу данных
#             # return HttpResponseRedirect(reverse('myadmin:productcategory_products', kwargs={'pk': pk}))
#             return HttpResponseRedirect(reverse('myadmin:productcategory_products', args=[pk]))
#     else:
#         form = ProductAdminUpdateForm(initial={'category': productcategory})
#     content = {
#         'title': 'админка/новый товар',
#         'form': form,
#     }
#     return render(request, 'adminapp/product_update.html', content)

@user_passes_test(lambda x: x.is_superuser)
def product_create(request, pk):
    productcategory = get_object_or_404(Categories, pk=pk)
    if request.method == 'POST':
        form = ProductAdminUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:productcategory_products', kwargs={'pk': pk}))
    else:
        form = ProductAdminUpdateForm()
    content = {
        'title': 'админка/новый товар',
        'form': form
    }
    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda x: x.is_superuser)
def product_update(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        form = ProductAdminUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  # приводит к сохранению в базу данных
            return HttpResponseRedirect(reverse('myadmin:productcategory_products', kwargs={'pk': product.category.pk}))
    else:
        form = ProductAdminUpdateForm(instance=product)

    content = {
        'title': 'админка/изменение товара',
        'form': form,
        'object': product,
    }

    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda x: x.is_superuser)
def product_delete(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('myadmin:productcategory_products', kwargs={'pk': product.category.pk}))
    elif request.method == 'GET':
        content = {
            'title': 'админка/удаление товара',
            'object': product,
        }
        return render(request, 'adminapp/product_delete.html', content)


# @user_passes_test(lambda x: x.is_superuser)
# def product_read(request, pk):
#     product = get_object_or_404(Products, pk=pk)
#     content = {
#         'title': 'админка/подробнее о товаре',
#         'object': product
#     }
#     return render(request, 'adminapp/product_read.html', content)


class ProductDetailView(DetailView):
    model = Products


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=Categories)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.products_set.update(is_active=True)
        else:
            instance.products_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
