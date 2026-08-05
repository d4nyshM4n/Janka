from django.shortcuts import render
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


    # Фильтр вегетарианских блюд

    vegetarian = request.GET.get("vegetarian")

    if vegetarian:

        dishes = dishes.filter(
            vegetarian=True
        )


    # Фильтр острых блюд

    spicy = request.GET.get("spicy")

    if spicy:

        dishes = dishes.filter(
            spicy=True
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
