from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
# Импортируем модель блюд (замени menu на имя своего приложения)
from menu.models import Dish 
from .models import Cart, CartItem


def _get_cart(request):
    """
    Вспомогательная функция: получает или создает корзину 
    для авторизованного пользователя или по ID сессии.
    """
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_id=session_id)
    return cart


@require_POST
def cart_add(request, dish_id):
    """Добавление блюда в корзину или изменение его количества."""
    cart = _get_cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    
    # Получаем количество из POST-запроса (по умолчанию 1)
    quantity = int(request.POST.get('quantity', 1))
    # Флаг: перезаписать количество или прибавить
    override = request.POST.get('override') == 'True'

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        dish=dish,
        defaults={'quantity': quantity}
    )

    if not created:
        if override:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, dish_id):
    """Удаление блюда из корзины."""
    cart = _get_cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    
    CartItem.objects.filter(cart=cart, dish=dish).delete()
    
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Отображение страницы корзины."""
    cart = _get_cart(request)
    # prefetch_related оптимизирует запросы к БД, чтобы страница грузилась быстро
    cart_items = cart.items.select_related('dish').all()

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)

