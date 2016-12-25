from django.shortcuts import render

def privacy(request):
    return render(request, 'static/privacy.html')

def terms(request):
    return render(request, 'static/terms.html')
