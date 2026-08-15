from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def contacts_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Спасибо! Ваше сообщение успешно отправлено. Мы ответим вам в ближайшее время.')
            return redirect('contacts:index')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'restaurant_address': 'г. Москва, ул. Тверская, д. 12',
        'restaurant_phone': '+7 (999) 123-45-67',
        'restaurant_email': 'info@janka-eco.ru',
        'working_hours': 'Пн-Вс: 10:00 — 23:00',
    }
    return render(request, 'contacts.html', context)