from celery import shared_task
from django.utils import timezone
from .models import Alarm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def check_alarms():
    now = timezone.now()
    current_time = now.time()
    current_day = now.strftime('%a')
    
    alarms = Alarm.objects.filter(is_active=True)

    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    for alarm in alarms:
        alarm_time = alarm.time
        
        time_diff = abs((alarm_time.hour * 60 + alarm_time.minute) - (current_time.hour * 60 + current_time.minute))
        
        if alarm.date and alarm.date == now.date():
            if time_diff <= 1:
                async_to_sync(channel_layer.group_send)(
                    f'user_{alarm.user_id or "anonymous"}',
                    {
                        'type': 'alarm_trigger',
                        'message': {
                            'id': alarm.id,
                            'time': alarm.time.strftime('%H:%M:%S'),
                            'date': str(alarm.date) if alarm.date else None,
                            'days': alarm.days,
                            'enabled': alarm.enabled,
                            'is_active': alarm.is_active,
                            'timezone': alarm.timezone,
                        }
                    }
                )
                alarm.is_active = False
                alarm.save()

        elif not alarm.date and current_day in alarm.days:
            if time_diff <= 1:
                async_to_sync(channel_layer.group_send)(
                    f'user_{alarm.user_id or "anonymous"}',
                    {
                        'type': 'alarm_trigger',
                        'message': {
                            'id': alarm.id,
                            'time': alarm.time.strftime('%H:%M:%S'),
                            'date': None,
                            'days': alarm.days,
                            'enabled': alarm.enabled,
                            'is_active': alarm.is_active,
                            'timezone': alarm.timezone,
                        }
                    }
                )