from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """
    Позволяет выводить блюда из заказа в виде аккуратной таблицы 
    прямо внутри страницы редактирования главного заказа.
    """
    model = OrderItem
    raw_id_fields = ['dish'] 
    extra = 0 


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Настройка отображения заказов в админ-панели Django"""
    list_display = [
        'id', 'first_name', 'phone', 'payment_method', 
        'paid', 'created_at', 'get_total_cost'
    ]
    list_display_links = ['id', 'first_name']
    list_filter = ['paid', 'payment_method', 'created_at', 'updated_at']
    search_fields = ['first_name', 'phone', 'address', 'comment']
    list_editable = ['paid']
    inlines = [OrderItemInline]

    def get_total_cost(self, obj):
        """Выводит общую стоимость заказа в общую таблицу админки"""
        return f"{obj.get_total_cost()} сом"
    get_total_cost.short_description = 'Сумма заказа'
