from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Добавили namespace='cart' для изоляции путей корзины
    path('cart/', include('cart.urls', namespace='cart')),
    path('reservation/', include('reservations.urls')),
    path('contacts/', include('contacts.urls')),
    path('', include('menu.urls')),
    path('order/', include('orders.urls', namespace='orders')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
