from ast import Str
from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Sneaker
from .forms import SneakerForm
from django.views.decorators.http import require_POST, require_safe, require_http_methods


# TODO: models, forms

@require_safe
def index(request):
    sneakers = Sneaker.objects.all()[1::-1]
    s_list = list(sneakers)
    # Banner 
    sn1 = s_list[0]
    sn2 = s_list[1]
    sn3 = s_list[2]

    context = {
        'sn1': sn1,
        'sn2': sn2,
        'sn3': sn3,
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


@require_safe
def detail(request, pk):
    sneaker = get_object_or_404(Sneaker, pk=pk)
    context = {
        'sneaker': sneaker,
    }
    return render(request, 'sneakers/detail.html', context=context)

@require_POST
def delete(request, pk):
    if request.user.is_authenticated():
        sneaker = get_object_or_404(pk=pk)
        sneaker.delete()
    return redirect('sneakers:index')

def update(request, pk):
    pass