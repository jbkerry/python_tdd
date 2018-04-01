from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Item


def home_page(request):
    return render(request, 'home.html')
    # return HttpResponse('<html><title>Cargo Selection</title></html>')


def view_cargo(request):
    items = Item.objects.all()

    return render(request, 'list.html', {'items': items})


def new_cargo(request):
    Item.objects.create(text=request.POST['cargo_text'])
    return redirect('/lists/the-only-list-in-the-world/')
