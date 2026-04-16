from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tovar, Zakaz, ZakazItem

class TovarModelTest(TestCase):
    def setUp(self):
        self.tovar = Tovar.objects.create(
            Vid_tovara='Тестовая пицца',
            Nomer_tovara=1001,
            Prace=500,
            category='pizza',
            description='Описание тестовой пиццы'
        )
    
    def test_tovar_creation(self):
        self.assertEqual(self.tovar.Vid_tovara, 'Тестовая пицца')
        self.assertEqual(self.tovar.Prace, 500)
    
    def test_tovar_str_method(self):
        self.assertEqual(str(self.tovar), 'Тестовая пицца')

class UserModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            FIO='Тестовый Пользователь',
            Number=1234567890,
            Address='Тестовый адрес',
            password='testpass123'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.FIO, 'Тестовый Пользователь')
        self.assertEqual(self.user.Number, 1234567890)
    
    def test_user_str_method(self):
        self.assertEqual(str(self.user), 'Тестовый Пользователь')

class ZakazModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            FIO='Тестовый Пользователь',
            Number=1234567890,
            Address='Тестовый адрес'
        )
        
        self.tovar = Tovar.objects.create(
            Vid_tovara='Тестовая пицца',
            Nomer_tovara=1001,
            Prace=500
        )
        
        self.zakaz = Zakaz.objects.create(
            user=self.user,
            Symma=1000,
            Sposob_oplati='card',
            status='new'
        )
        
        self.zakaz_item = ZakazItem.objects.create(
            zakaz=self.zakaz,
            tovar=self.tovar,
            quantity=2,
            price=500
        )
    
    def test_zakaz_creation(self):
        self.assertEqual(self.zakaz.Symma, 1000)
        self.assertEqual(self.zakaz.status, 'new')
    
    def test_zakaz_item_creation(self):
        self.assertEqual(self.zakaz_item.quantity, 2)
        self.assertEqual(self.zakaz_item.price, 500)
    
    def test_zakaz_str_method(self):
        self.assertIn('Заказ #', str(self.zakaz))