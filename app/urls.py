from django.urls import path
from . import views

urlpatterns = [
    # Главная страница и навигация
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('catalog/', views.catalog, name='catalog'),
    
    # Корзина
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:tovar_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:tovar_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Аккаунт
    path('account/', views.account, name='account'),
    path('account/edit/', views.account_edit, name='account_edit'),
    
    # Аутентификация
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Товары
    path('tovars/', views.tovar_list, name='tovar_list'),
    path('tovars/<int:pk>/', views.tovar_detail, name='tovar_detail'),
    path('tovars/create/', views.tovar_create, name='tovar_create'),
    path('tovars/<int:pk>/update/', views.tovar_update, name='tovar_update'),
    
    # Пользователи
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    
    # Заказы
    path('zakazs/', views.zakaz_list, name='zakaz_list'),
    path('zakazs/<int:pk>/', views.zakaz_detail, name='zakaz_detail'),
    path('zakazs/create/', views.zakaz_create, name='zakaz_create'),
    path('zakazs/<int:pk>/update/', views.zakaz_update, name='zakaz_update'),
]