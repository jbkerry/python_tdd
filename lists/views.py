from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import Item, List

User = get_user_model()


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
    form = NewListForm(data=request.POST)
    if form.is_valid():
        cargo_list = form.save(owner=request.user)
        return redirect(cargo_list)
    return render(request, 'home.html', {'form': form})


def my_cargo(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_cargo.html', {'owner': owner})


def share_cargo(request, cargo_list_id):
    cargo_list = List.objects.get(id=cargo_list_id)
    cargo_list.shared_with.add(request.POST['sharee'])

    return redirect(cargo_list)
