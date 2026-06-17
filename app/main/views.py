from django.shortcuts import render
from .models import*

def main(request):
    assembled = AssembledWeapon.objects.all()
    return render(request, "pages/main.html", {"assembled" : assembled, "allWeapon" : Weapon.objects.all()})

def weapon(request, weapon):
    assembled = Weapon.objects.get(title=weapon).assembledweapon_set.all()
    return render(request, "pages/main.html", {"assembled" : assembled, "allWeapon" : Weapon.objects.all()})
