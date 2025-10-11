from django.shortcuts import render
from django.http import HttpResponse

def payment(request):
    return HttpResponse("This is a payment Page ! ")


def esewa_payment(request):
    return HttpResponse("This is esewa payment gateway ! ")