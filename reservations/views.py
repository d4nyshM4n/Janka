from django.shortcuts import render
from .models import Reservation


def reserve(request):

    if request.method == 'POST':

        Reservation.objects.create(

            name=request.POST.get('name'),

            phone=request.POST.get('phone'),

            date=request.POST.get('date'),

            time=request.POST.get('time'),

            guests=request.POST.get('guests'),

            comment=request.POST.get('comment')

        )

        return render(request, 'reservation_success.html')

    return render(request, 'reservation.html')