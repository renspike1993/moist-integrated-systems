from django.shortcuts import render

def get_dashboard(request):
    return render(request,'base.html')

def get_program(request):
    return render(request,'program/list.html')