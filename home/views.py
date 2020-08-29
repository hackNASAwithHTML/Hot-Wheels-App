from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from diecast.models import DieCastModel
# Create your views here.

def home(request):
    diecast = DieCastModel.objects.all()
    return render(request,"home.html",{"diecast_list":diecast})
@login_required(login_url='/login/')
def car_culture(request):
    return render(request,"car_culture.html")
@login_required(login_url='/login/')
def red_line_club(request):
    return render(request,"red_line_club.html")
@login_required(login_url='/login/')
def super_treasure_hunt(request):
    return render(request,"super_treasure_hunt.html")