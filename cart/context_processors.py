def cart(request):
    from .models import Cart
    if not request.session.session_key:
        request.session.create()
    
    session_id = request.session.session_key

    try:
        if request.user.is_authenticated:
            cart_obj = Cart.objects.filter(user=request.user).first()
        else:
            cart_obj = Cart.objects.filter(session_id=session_id).first()
    except Exception:
        cart_obj = None
    return {'cart': cart_obj}
