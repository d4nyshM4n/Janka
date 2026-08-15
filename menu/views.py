from django.shortcuts import render, get_object_or_404
from .models import Dish, Category

def home(request):
    dishes = Dish.objects.filter(
        available=True
    )[:6]

    context = {
        "dishes": dishes,
    }

    return render(
        request,
        "home.html",
        context
    )


def menu(request):
    categories = Category.objects.all()
    dishes = Dish.objects.filter(
        available=True
    )

    breakfast = request.GET.get("breakfast")
    if breakfast:
        dishes = dishes.filter(
            breakfast=True
        )

    soup = request.GET.get("soup")
    if soup:
        dishes = dishes.filter(
            soup=True
        )

    main = request.GET.get("main")
    if main:
        dishes = dishes.filter(
            main=True
        )

    salats = request.GET.get("salats")
    if salats:
        dishes = dishes.filter(
            salats=True
        )

    deserts = request.GET.get("deserts")
    if deserts:
        dishes = dishes.filter(
            deserts=True
        )

    drinks = request.GET.get("drinks")
    if drinks:
        dishes = dishes.filter(
            drinks=True
        )    

    context = {
        "categories": categories,
        "dishes": dishes,
    }

    return render(
        request,
        "menu.html",
        context
    )


def dish(request, id):
    dish = get_object_or_404(
        Dish,
        id=id
    )

    context = {
        "dish": dish
    }

    return render(
        request,
        "dish.html",
        context
    )


def about(request):
    return render(request, 'about.html')
