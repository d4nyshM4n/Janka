from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from menu.models import Dish 

def _get_cart(request):
    """
    Вспомогательная функция: получает или создает корзину 
    для авторизованного пользователя или по ID сессии.
    """
    from .models import Cart

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
    from .models import CartItem

    cart = _get_cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1
    override = request.POST.get('override') == 'True'

    if override and quantity <= 0:
        CartItem.objects.filter(cart=cart, dish=dish).delete()
        if not cart.items.exists():
            cart.delete()
        return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))

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
        if cart_item.quantity <= 0:
            cart_item.delete()
            if not cart.items.exists():
                cart.delete()
        else:
            cart_item.save()

    return redirect(request.META.get('HTTP_REFERER', 'menu:menu'))


@require_POST
def cart_remove(request, dish_id):
    """Удаление блюда из корзины."""
    from .models import CartItem

    cart = _get_cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    
    # Удаляем выбранную позицию
    CartItem.objects.filter(cart=cart, dish=dish).delete()
    if not cart.items.exists():
        cart.delete()
    
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Отображение страницы корзины."""
    cart = _get_cart(request)
    cart_items = cart.items.select_related('dish').all()

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)
