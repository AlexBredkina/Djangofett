from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name = 'index'),
    # path('users/', adminapp.admin_users, name = 'admin_users'),
    path('users/', adminapp.UserListView.as_view(), name='admin_users'),
    # path('users/create', adminapp.admin_users_create, name = 'admin_users_create'),
    path('users/create', adminapp.UserCreateView.as_view(), name='admin_users_create'),
    # path('users/update/<int:user_id>/', adminapp.admin_users_update, name = 'admin_users_update'),
    path('users/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='admin_users_update'),
    # path('users/remove/<int:user_id>/', adminapp.admin_users_remove, name = 'admin_users_remove'),
    path('users/remove/<int:pk>/', adminapp.UserDeleteView.as_view(), name='admin_users_remove'),
    # path('products/', adminapp.admin_products, name = 'admin_products'),
    path('products/', adminapp.ProductListView.as_view(), name='admin_products'),
    path('products/create', adminapp.admin_products_create, name = 'admin_products_create'),
    path('products/update/<int:product_id>/', adminapp.admin_products_update, name = 'admin_products_update'),
    path('products/remove/<int:product_id>/', adminapp.admin_products_remove, name = 'admin_products_remove'),
    # path('categories/', adminapp.admin_categories, name='admin_categories'),
    path('categories/', adminapp.CategoryListView.as_view(), name='admin_categories'),
    path('categories/create', adminapp.admin_categories_create, name='admin_categories_create'),
    path('categories/update/<int:cat_id>/', adminapp.admin_categories_update, name='admin_categories_update'),
    path('categories/remove/<int:cat_id>/', adminapp.admin_categories_remove, name='admin_categories_remove'),


]