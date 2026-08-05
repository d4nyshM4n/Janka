from django.db import models
from django.conf import settings
# Замени 'menu' и 'Dish' на имя своего приложения и модели блюд
from menu.models import Dish 


class Cart(models.Model):
    """Модель корзины пользователя"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    session_id = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name='ID сессии (для неавторизованных)'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        if self.user:
            return f'Корзина пользователя {self.user}'
        return f'Корзина (Сессия: {self.session_id})'

    def get_total_price(self):
        """Подсчет общей стоимости всех позиций в корзине"""
        return sum(item.get_cost() for item in self.items.all())

    def get_total_quantity(self):
        """Подсчет общего количества порций"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Модель элемента/блюда в корзине"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Блюдо'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        # Гарантирует, что одно и то же блюдо не будет дублироваться строками, а увеличится quantity
        unique_together = ('cart', 'dish') 

    def __str__(self):
        return f'{self.quantity} x {self.dish.name}'

    def get_cost(self):
        """Стоимость одной позиции (цена блюда * количество)"""
        return self.dish.price * self.quantity  