from django.shortcuts import render
from destinations.models import Region


def home(request):
    regions = Region.objects.prefetch_related('cities').all()
    return render(request,'home.html',{'regions':regions})
