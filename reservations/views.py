from django.shortcuts import render
from .models import Reservation
from .forms import ReservationForm
from .whatsapp import send_booking_to_whatsapp


def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            send_booking_to_whatsapp(reservation)
            return render(request, 'reservations/reservation_success.html', {
                'reservation': reservation
            })
    else:
        form = ReservationForm()
        
    return render(request, 'reservations/reservation_form.html', {'form': form})


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