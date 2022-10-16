from ast import Str
from multiprocessing import context
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Sneaker, Images
from .forms import SneakerForm
from .serializer.sneakers import SneakerListSerializer, SneakerSerializer
from django.views.decorators.http import require_POST, require_safe, require_http_methods


# TODO: models, forms

@require_safe
def index(request):
    sneakers = Sneaker.objects.all()[1::-1]
    # sneakers = get_list_or_404(Sneaker)
    # Banner 
    sn1 = sneakers[0]
    sn2 = sneakers[1]
    sn3 = sneakers[2]
    
    sn1_img = Images.objects.filter(sneaker_id = sn1.id)[0]
    sn2_img = Images.objects.filter(sneaker_id = sn2.id)[0]
    sn3_img = Images.objects.filter(sneaker_id = sn3.id)[0]

    context = {
        'sn1': sn1, 
        'sn2': sn2,
        'sn3': sn3,
        'sn1_img': sn1_img,
        'sn2_img': sn2_img,
        'sn3_img': sn3_img,
        
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
            
            for img in request.FILES.getlist('imgs'):
                image = Images()
                image.sneaker = sneaker # foreignKey
                image.image = img
                image.save()
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

@api_view(['GET'])
def v1_index(request):
    sneaker = get_object_or_404(Sneaker, pk=1)
    serializer = SneakerSerializer(sneaker)
    
    return Response(serializer.data)
    
@api_view(['GET', 'POST'])
def v1_create(request):
    if request.method == 'POST':
        serializer = SneakerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errorsm, status=status.HTTP_400_BAD_REQUEST)