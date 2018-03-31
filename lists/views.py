from django.shortcuts import render


def home_page(request):
    return render(request, 'home.html')
    # return HttpResponse('<html><title>Cargo Selection</title></html>')
