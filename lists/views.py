from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Item, List


def home_page(request):
    return render(request, 'home.html')
    # return HttpResponse('<html><title>Cargo Selection</title></html>')


def view_cargo(request, cargo_list_id):
    cargo_list = List.objects.get(id=cargo_list_id)
    return render(request, 'list.html', {'cargo_list': cargo_list})


def new_cargo(request):
    cargo_list = List.objects.create()
    Item.objects.create(text=request.POST['cargo_text'], list=cargo_list)
    return redirect(f'/lists/{cargo_list.id}/')


def add_cargo(request, cargo_list_id):
    cargo_list = List.objects.get(id=cargo_list_id)
    Item.objects.create(text=request.POST['cargo_text'], list=cargo_list)

    return redirect(f'/lists/{cargo_list.id}/')
