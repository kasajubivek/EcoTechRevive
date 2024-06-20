
from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import models


def aboutus_view(request):
    return render(request,'aboutus.html')

# Create your views here.

