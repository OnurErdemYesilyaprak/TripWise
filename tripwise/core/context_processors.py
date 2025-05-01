from destinations.models import Region

def regions_context(request):
    regions = Region.objects.prefetch_related('cities').all()
    return {'regions': regions}
