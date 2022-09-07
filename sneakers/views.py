from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Sneaker
from .forms import SneakerForm


# TODO: models, forms

def index(request):
    sneakers = Sneaker.objects.all()
    context = {
        'sneakers': sneakers,
    }
    return render(request, 'sneakers/index.html', context=context)
@login_required
def create(request):
    if request.method == 'POST':
        form = SneakerForm(request.POST, request.FILES)
        if form.is_valid():
            sneaker = form.save(commit=False)
            sneaker.user = request.user
            sneaker.save()
            return redirect('sneakers:index')
    else:
        form = SneakerForm()
    context = {
        'form': form,
    }
    return render(request, 'sneakers/create.html', context=context)

def update(request, id):
    pass

def detail(request, id):
    pass