
from django.http import JsonResponse

# Create your views here.


def sendAttendance(request):
    context: dict = {}

    return JsonResponse(request.GET)
