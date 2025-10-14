from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def in_home(request):
    return render(request,'Home/Landing_page/landing_page.html')
