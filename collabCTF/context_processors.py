from competition.models import Competition


def ctf_sidebar(request):
    return {'sidebar': {'ctfs': Competition.objects.only('name', 'slug')}}