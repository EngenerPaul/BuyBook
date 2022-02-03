from django.http import HttpResponse
from django.shortcuts import render

def first_func(request):
    template_name = 'buybook/index.html'
    content = {
        'hello' : 'hello world'
    }
    return render(request, template_name, content)