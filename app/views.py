from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import User, Tovar, Zakaz, ZakazItem
from .forms import UserRegisterForm, UserForm, TovarForm, ZakazForm

# Главная страница
def index(request):
    popular_tovars = Tovar.objects.all()[:6]
    pizzas = Tovar.objects.filter(category='pizza')[:3]
    return render(request, 'app/index.html', {
        'popular_tovars': popular_tovars,
        'pizzas': pizzas
    })

# О нас
def about(request):
    return render(request, 'app/about.html')

# Каталог товаров
def catalog(request):
    category = request.GET.get('category', 'all')
    search = request.GET.get('search', '')
    
    tovars = Tovar.objects.all()
    
    if category != 'all':
        tovars = tovars.filter(category=category)
    
    if search:
        tovars = tovars.filter(Q(Vid_tovara__icontains=search) | Q(description__icontains=search))
    
    categories = dict(Tovar.CATEGORY_CHOICES)
    
    return render(request, 'app/catalog.html', {
        'tovars': tovars,
        'current_category': category,
        'categories': categories,
        'search': search
    })

# Корзина
@login_required
def cart(request):
    cart_items = request.session.get('cart', {})
    tovars = []
    total = 0
    
    for tovar_id, quantity in cart_items.items():
        tovar = Tovar.objects.get(id=tovar_id)
        tovars.append({
            'tovar': tovar,
            'quantity': quantity,
            'subtotal': tovar.Prace * quantity
        })
        total += tovar.Prace * quantity
    
    return render(request, 'app/cart.html', {
        'cart_items': tovars,
        'total': total
    })

@login_required
def add_to_cart(request, tovar_id):
    cart = request.session.get('cart', {})
    cart[str(tovar_id)] = cart.get(str(tovar_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, 'Товар добавлен в корзину!')
    return redirect('catalog')

@login_required
def remove_from_cart(request, tovar_id):
    cart = request.session.get('cart', {})
    if str(tovar_id) in cart:
        del cart[str(tovar_id)]
        request.session['cart'] = cart
        messages.success(request, 'Товар удален из корзины!')
    return redirect('cart')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Корзина пуста!')
        return redirect('catalog')
    
    if request.method == 'POST':
        form = ZakazForm(request.POST)
        if form.is_valid():
            zakaz = form.save(commit=False)
            zakaz.user = request.user
            zakaz.save()
            
            total = 0
            for tovar_id, quantity in cart.items():
                tovar = Tovar.objects.get(id=tovar_id)
                ZakazItem.objects.create(
                    zakaz=zakaz,
                    tovar=tovar,
                    quantity=quantity,
                    price=tovar.Prace
                )
                total += tovar.Prace * quantity
            
            zakaz.Symma = total
            zakaz.save()
            
            request.session['cart'] = {}
            messages.success(request, 'Заказ успешно оформлен!')
            return redirect('zakaz_detail', pk=zakaz.id)
    else:
        form = ZakazForm(initial={'user': request.user})
    
    return render(request, 'app/checkout.html', {'form': form})

# Аккаунт пользователя
@login_required
def account(request):
    user_orders = Zakaz.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'app/account.html', {'orders': user_orders})

@login_required
def account_edit(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные обновлены!')
            return redirect('account')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'app/account_edit.html', {'form': form})

# Аутентификация
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.FIO}!')
            return redirect('index')
        else:
            messages.error(request, 'Неверный логин или пароль!')
    return render(request, 'app/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта!')
    return redirect('index')

# CRUD для Товаров
def tovar_list(request):
    tovars = Tovar.objects.all()
    return render(request, 'app/tovar_list.html', {'tovars': tovars})

def tovar_detail(request, pk):
    tovar = get_object_or_404(Tovar, pk=pk)
    return render(request, 'app/tovar_detail.html', {'tovar': tovar})

@login_required
def tovar_create(request):
    if request.method == 'POST':
        form = TovarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно добавлен!')
            return redirect('tovar_list')
    else:
        form = TovarForm()
    return render(request, 'app/tovar_form.html', {'form': form, 'title': 'Добавить товар'})

@login_required
def tovar_update(request, pk):
    tovar = get_object_or_404(Tovar, pk=pk)
    if request.method == 'POST':
        form = TovarForm(request.POST, instance=tovar)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно обновлен!')
            return redirect('tovar_list')
    else:
        form = TovarForm(instance=tovar)
    return render(request, 'app/tovar_form.html', {'form': form, 'title': 'Редактировать товар'})

# CRUD для Пользователей
@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'app/user_list.html', {'users': users})

@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'app/user_detail.html', {'user': user})

@login_required
def user_create(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно добавлен!')
            return redirect('user_list')
    else:
        form = UserRegisterForm()
    return render(request, 'app/user_form.html', {'form': form, 'title': 'Добавить пользователя'})

@login_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно обновлен!')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'app/user_form.html', {'form': form, 'title': 'Редактировать пользователя'})

# CRUD для Заказов
@login_required
def zakaz_list(request):
    zakazs = Zakaz.objects.all()
    return render(request, 'app/zakaz_list.html', {'zakazs': zakazs})

@login_required
def zakaz_detail(request, pk):
    zakaz = get_object_or_404(Zakaz, pk=pk)
    items = ZakazItem.objects.filter(zakaz=zakaz)
    return render(request, 'app/zakaz_detail.html', {'zakaz': zakaz, 'items': items})

@login_required
def zakaz_create(request):
    if request.method == 'POST':
        form = ZakazForm(request.POST)
        if form.is_valid():
            zakaz = form.save()
            messages.success(request, 'Заказ успешно создан!')
            return redirect('zakaz_list')
    else:
        form = ZakazForm()
    return render(request, 'app/zakaz_form.html', {'form': form, 'title': 'Создать заказ'})

@login_required
def zakaz_update(request, pk):
    zakaz = get_object_or_404(Zakaz, pk=pk)
    if request.method == 'POST':
        form = ZakazForm(request.POST, instance=zakaz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заказ успешно обновлен!')
            return redirect('zakaz_list')
    else:
        form = ZakazForm(instance=zakaz)
    return render(request, 'app/zakaz_form.html', {'form': form, 'title': 'Редактировать заказ'})