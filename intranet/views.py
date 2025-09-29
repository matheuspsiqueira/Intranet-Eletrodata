from django.shortcuts import render

def index(request):
    return render (request, 'index.html')

def etica_compliance(request):
    return render (request, 'etica_compliance.html')