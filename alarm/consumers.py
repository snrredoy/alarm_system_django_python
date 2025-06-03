# # alarms/consumers.py
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class AlarmConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         user_id = self.scope['url_route']['kwargs'].get('user_id', 'anonymous')
#         self.group_name = f'user_{user_id}'
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def alarm_trigger(self, event):
#         await self.send(text_data=json.dumps({
#             'type': 'alarm_trigger',
#             'message': event['message']
#         }))

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AlarmConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['url_route']['kwargs'].get('user_id', 'anonymous')
        self.group_name = f'user_{user_id}'
        print("WebSocket connected for group", self.group_name)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print("WebSocket disconnected for group", self.group_name)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def alarm_trigger(self, event):
        print("Sending alarm_trigger to group", self.group_name, ":", event['message'])
        await self.send(text_data=json.dumps({
            'type': 'alarm_trigger',
            'message': {
                'time': event['message']['time'],
                'date': event['message']['date'],
                'days': event['message']['days'],
                'enabled': event['message']['enabled'],
                'is_active': event['message']['is_active'],
                'timezone': event['message']['timezone'],
            },
        }))
    