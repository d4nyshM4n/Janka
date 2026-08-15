from django.shortcuts import render, redirect, get_object_or_404
from cart.views import _get_cart 
from .models import OrderItem, Order

def order_create(request):
    """Контроллер обработки и оформления заказа"""
    cart = _get_cart(request)
    cart_items = cart.items.select_related('dish').all()
    if not cart_items.exists():
        return redirect('menu')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method', 'cash')
        comment = request.POST.get('comment', '')
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_id=request.session.session_key,
            first_name=first_name,
            phone=phone,
            address=address,
            payment_method=payment_method,
            comment=comment
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                dish=item.dish,
                price=item.dish.price, 
                quantity=item.quantity
            )
        cart.items.all().delete()
        cart.delete()
        request.session['order_id'] = order.id
        return redirect('orders:order_success')
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    return render(request, 'order_create.html', context)


def order_success(request):
    """Страница успешного завершения заказа"""
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id) if order_id else None
    if 'order_id' in request.session:
        del request.session['order_id']

    return render(request, 'order_success.html', {'order': order})
