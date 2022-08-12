from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
# TODO: models, forms

def index(request):
    """
    1. Main index page 
    Args :
        
    Returns :
        index.html,
        sneakers List,
        Raffle List
    """
    context = {
        
    }
    return render(request, 'sneakers/index.html', context=context)

