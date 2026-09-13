from django.conf import settings

def environment(request):
    env = getattr(settings, 'ENVIRONMENT', 'PROD')
    return {
        'ENVIRONMENT': env,
    }