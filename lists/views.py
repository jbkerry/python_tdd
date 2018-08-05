from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.forms import ExistingListItemForm, ItemForm
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})
    # return HttpResponse('<html><title>Cargo Selection</title></html>')


def view_cargo(request, cargo_list_id):
    cargo_list = List.objects.get(id=cargo_list_id)
    form = ExistingListItemForm(for_list=cargo_list)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=cargo_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(cargo_list)
    return render(request, 'list.html', {'cargo_list': cargo_list, 'form': form})


def new_cargo(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        cargo_list = List.objects.create()
        form.save(for_list=cargo_list)
        return redirect(cargo_list)
    else:
        return render(request, 'home.html', {'form': form})
