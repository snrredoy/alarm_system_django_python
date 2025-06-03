from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Alarm
from .serializers import AlarmSerializer
from django.shortcuts import get_object_or_404

class AlarmListCreateView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id', 'anonymous')
        alarms = Alarm.objects.filter(user_id=user_id)
        serializer = AlarmSerializer(alarms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AlarmSerializer(data=request.data)
        if serializer.is_valid():
            if 'Everyday' in request.data.get('days', []):
                serializer.validated_data['days'] = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            serializer.save(user_id=request.data.get('user_id', 'anonymous'))
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlarmDetailView(APIView):
    def get(self, request, pk):
        alarm = get_object_or_404(Alarm, pk=pk)
        serializer = AlarmSerializer(alarm)
        return Response(serializer.data)

    def put(self, request, pk):
        alarm = get_object_or_404(Alarm, pk=pk)
        serializer = AlarmSerializer(alarm, data=request.data, partial=True)
        if serializer.is_valid():
            if 'Everyday' in request.data.get('days', []):
                serializer.validated_data['days'] = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            serializer.save(user_id=request.data.get('user_id', 'anonymous'))
            return Response({'status': 'success'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        alarm = get_object_or_404(Alarm, pk=pk)
        alarm.delete()
        return Response({'status': 'success'}, status=status.HTTP_204_NO_CONTENT)

class AlarmToggleView(APIView):
    def patch(self, request, pk):
        alarm = get_object_or_404(Alarm, pk=pk)
        alarm.enabled = not alarm.enabled
        alarm.save()
        return Response({'status': 'success', 'enabled': alarm.enabled})
