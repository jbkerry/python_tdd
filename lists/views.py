from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})
    # return HttpResponse('<html><title>Cargo Selection</title></html>')


def view_cargo(request, cargo_list_id):
    cargo_list = List.objects.get(id=cargo_list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['text'], list=cargo_list)
            item.full_clean()
            item.save()
            return redirect(cargo_list)
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, 'list.html', {'cargo_list': cargo_list, 'error': error})


def new_cargo(request):
    cargo_list = List.objects.create()
    item = Item(text=request.POST['text'], list=cargo_list)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        cargo_list.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(cargo_list)
