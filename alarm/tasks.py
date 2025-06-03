# from celery import shared_task
# from django.utils import timezone
# from .models import Alarm
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync

# @shared_task
# def check_alarms():
#     now = timezone.now()
#     current_time = now.time()
#     current_day = now.strftime('%a')
#     print("current_time", current_time)
#     print("current_day", current_day)
#     alarms = Alarm.objects.filter(is_active=True)
#     print("alarms", alarms)
#     channel_layer = get_channel_layer()

#     for alarm in alarms:
#         alarm_time = alarm.time
#         print("alarm_time", alarm_time)
#         if alarm.date and alarm.date == now.date():
#             print("date")
#             if alarm_time.hour == current_time.hour and alarm_time.minute == current_time.minute:
#                 async_to_sync(channel_layer.group_send)(
#                     f'user_{alarm.user_id or "anonymous"}',
#                     {
#                         'type': 'alarm_trigger',
#                         'message': {
#                             'id': alarm.id,
#                             'time': alarm.time.strftime('%H:%M'),
#                             'date': str(alarm.date) if alarm.date else None,
#                             'days': alarm.days
#                         }
#                     }
#                 )
#                 alarm.is_active = False
#                 alarm.save()
#         elif not alarm.date and current_day in alarm.days:
#             print("day")
#             if alarm_time.hour == current_time.hour and alarm_time.minute == current_time.minute:
#                 async_to_sync(channel_layer.group_send)(
#                     f'user_{alarm.user_id or "anonymous"}',
#                     {
#                         'type': 'alarm_trigger',
#                         'message': {
#                             'id': alarm.id,
#                             'time': alarm.time.strftime('%H:%M'),
#                             'date': None,
#                             'days': alarm.days
#                         }
#                     }
#                 )

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
    print("Checking alarms at", now, "(time:", current_time, ", day:", current_day, ")")
    
    alarms = Alarm.objects.filter(is_active=True)
    print("Found", len(alarms), "active alarms:", [f"Alarm {a.id} at {a.time} on {a.date or a.days}" for a in alarms])

    channel_layer = get_channel_layer()
    if channel_layer is None:
        print("Error: Channel layer is None, cannot send WebSocket messages")
        return

    for alarm in alarms:
        alarm_time = alarm.time
        print("Checking alarm", alarm.id, ": user_id=", alarm.user_id, ", time=", alarm_time, ", date=", alarm.date, ", days=", alarm.days)
        
        # Calculate time difference in minutes
        time_diff = abs((alarm_time.hour * 60 + alarm_time.minute) - (current_time.hour * 60 + current_time.minute))
        print("Time difference for alarm", alarm.id, ":", time_diff, "minutes")
        
        if alarm.date and alarm.date == now.date():
            print("Alarm", alarm.id, "has date", alarm.date)
            if time_diff <= 1:  # Trigger within ±1 minute
                print("Alarm", alarm.id, "triggered for date", alarm.date, "at", alarm_time)
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
                print("Sent WebSocket message for alarm", alarm.id, "to group user_", alarm.user_id or "anonymous")
                alarm.is_active = False
                alarm.save()
                print("Alarm", alarm.id, "deactivated")
        elif not alarm.date and current_day in alarm.days:
            print("Alarm", alarm.id, "has day", current_day)
            if time_diff <= 1:
                print("Alarm", alarm.id, "triggered for day", current_day, "at", alarm_time)
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
                print("Sent WebSocket message for alarm", alarm.id, "to group user_", alarm.user_id or "anonymous")