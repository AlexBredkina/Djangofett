from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.models import User
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, ProductAdminRegisterForm, ProductAdminChangeForm,CategoryAdminRegisterForm,CategoryAdminChangeForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from mainapp.models import ProductCategory, Product

from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.
@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'adminapp/index.html')

class UserListView(ListView):
    model = User
    template_name = 'adminapp/admin-users-read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)



# @user_passes_test(lambda u: u.is_superuser)
# def admin_users(request):
#     context = {
#         'users': User.objects.all(),
#     }
#     return render(request, 'adminapp/admin-users-read.html', context)

class UserCreateView(CreateView):
    model = User
    template_name = 'adminapp/admin-users-create.html'
    success_url = reverse_lazy('adminapp:admin_users')
    form_class = UserAdminRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)



# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:admin_users'))
#     else:
#         form = UserAdminRegisterForm()
#     context = {'form': form}
#     return render(request, 'adminapp/admin-users-create.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_update(request, user_id):
#     user = User.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users'))
#     else:
#         form = UserAdminProfileForm(instance=user)
#
#     context = {
#         'form': form,
#         'user': user
#     }
#     return render(request, 'adminapp/admin-users-update-delete.html', context)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('adminapp:admin_users')
    form_class = UserAdminProfileForm

    def get_context_data(self, **kwargs):
        context= super(UserUpdateView,self).get_context_data(**kwargs)
        context['title'] = 'GeekShop USER UPDATE'
        return context



#
# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_remove(request, user_id):
#     user = User.objects.get(id=user_id)
#     user.is_active = False
#     user.save()
#     return HttpResponseRedirect(reverse('admin_staff:admin_users'))

class UserDeleteView(DeleteView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('adminapp:admin_users')


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())




# def admin_products(request):
#     context = {
#         'products': Product.objects.all(),
#     }
#     # product = get_object_or_404(Product, pk=pk)
#     # context = {'product': product, }
#     return render(request, 'adminapp/admin-product-read.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/admin-product-read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductListView, self).dispatch(request, *args, **kwargs)



def admin_products_create(request):
    if request.method == 'POST':
        form = ProductAdminRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:admin_products'))
    else:
        form = ProductAdminRegisterForm()
    context = {'form': form}
    # category = get_object_or_404(ProductCategory, pk=pk)
    # if request.method == 'POST':
    #     form = ProductAdminRegisterForm(data=request.POST, files=request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(reverse('adminapp:admin_products', args=[pk]))
    # else:
    #     form = ProductAdminRegisterForm()
    # content = {
    #     'form': form,
    #     'category': category,
    # }

    return render(request, 'adminapp/admin-products-create.html', context)


def admin_products_update(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductAdminChangeForm(data=request.POST, files=request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_products'))
    else:
        form = ProductAdminChangeForm(instance=product)

    context = {
        'form': form,
        'product': product
    }
    return render(request, 'adminapp/admin-products-update-delete.html', context)


def admin_products_remove(request, product_id):
    product = Product.objects.get(id=product_id)
    product.is_active = False
    product.save()
    return HttpResponseRedirect(reverse('admin_staff:admin_products'))

# def admin_products_update(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         form = ProductAdminChangeForm(request.POST, request.FILES,
#                                       instance=product)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_products',
#                                                 args=[product.pk]))
#     else:
#         form = ProductAdminChangeForm(instance=product)
#
#     content = {'form': form,
#                'category': product.category
#                }
#
#     return render(request, 'adminapp/admin-products-update-delete.html', content)


# def admin_products_remove(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     product.is_active = False
#     product.save()
#     return HttpResponseRedirect(reverse('admin_staff:admin_products', args=[product.category.pk]))
# def admin_categories(request):
#     context = {
#         'categories': ProductCategory.objects.all(),
#     }
#     return render(request, 'adminapp/admin-category-read.html', context)


class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/admin-category-read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryListView, self).dispatch(request, *args, **kwargs)


def admin_categories_create(request):
    if request.method == 'POST':
        form = CategoryAdminRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:admin_categories'))
    else:
        form = CategoryAdminRegisterForm()
    context = {'form': form}
    return render(request, 'adminapp/admin-category-create.html', context)


def admin_categories_remove(request, cat_id):
    category = ProductCategory.objects.get(id=cat_id)
    category.is_active = False
    category.save()
    return HttpResponseRedirect(reverse('admin_staff:admin_categories'))



def admin_categories_update(request, cat_id):
    category = ProductCategory.objects.get(id=cat_id)
    if request.method == 'POST':
        form = CategoryAdminChangeForm(data=request.POST, files=request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_categories'))
    else:
        form = CategoryAdminChangeForm(instance=category)

    context = {
        'form': form,
        'category': category
    }
    return render(request, 'adminapp/admin-category-update-delete.html', context)