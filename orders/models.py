from django.db import models
from django.conf import settings
from menu.models import Dish

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Наличными курьеру'),
        ('card', 'Картой курьеру (терминал)'),
        ('online', 'Элсом / О!Деньги'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    session_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='ID сессии гостя')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    address = models.CharField(max_length=250, verbose_name='Адрес доставки')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash', verbose_name='Способ оплаты')
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id}'

    def get_total_cost(self):
        """Подсчет общей суммы заказа"""
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='order_items', verbose_name='Блюдо')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена на момент заказа')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity
