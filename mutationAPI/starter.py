from django.views.generic import View
from django.http import JsonResponse

class Starter(View):
    """
    Esta vista sirve solamente para consultar si el servicio se encuentra activo.
    """
    def get(self, request):
        json_object = {'info': "API Service Ready", 'api-documentation': '/api/doc/'}
        return JsonResponse(json_object)
