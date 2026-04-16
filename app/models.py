from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    FIO = models.CharField(max_length=100, verbose_name="ФИО")
    Number = models.IntegerField(verbose_name="Номер телефона")
    Address = models.CharField(max_length=255, verbose_name="Адрес")
    
    def __str__(self):
        return self.FIO
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Tovar(models.Model):
    CATEGORY_CHOICES = [
        ('pizza', 'Пицца'),
        ('drink', 'Напитки'),
        ('snack', 'Закуски'),
        ('dessert', 'Десерты'),
    ]
    
    Vid_tovara = models.CharField(max_length=200, verbose_name="Название товара")
    Nomer_tovara = models.IntegerField(verbose_name="Артикул")
    Prace = models.IntegerField(verbose_name="Цена")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='pizza', verbose_name="Категория")
    description = models.TextField(verbose_name="Описание", blank=True)
    
    def __str__(self):
        return self.Vid_tovara
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class Zakaz(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('online', 'Онлайн'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('delivery', 'Доставка'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]
    
    Symma = models.IntegerField(verbose_name="Сумма заказа")
    Sposob_oplati = models.CharField(max_length=50, choices=PAYMENT_METHODS, verbose_name="Способ оплаты")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    tovar = models.ManyToManyField(Tovar, through='ZakazItem', verbose_name="Товары")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.user.FIO}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class ZakazItem(models.Model):
    zakaz = models.ForeignKey(Zakaz, on_delete=models.CASCADE, verbose_name="Заказ")
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(default=1, verbose_name="Количество")
    price = models.IntegerField(verbose_name="Цена")
    
    def __str__(self):
        return f"{self.tovar.Vid_tovara} x {self.quantity}"