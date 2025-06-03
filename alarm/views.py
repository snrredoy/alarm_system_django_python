from django.shortcuts import render

# Create your views here.
def alarm_view(request):
    return render(request, 'alarm.html')
