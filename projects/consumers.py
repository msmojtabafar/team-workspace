import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from tasks.models import Task

class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.room_group_name = f'project_{self.project_id}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'task_update':
            task_id = text_data_json['task_id']
            new_status = text_data_json['status']
            
            task = await self.update_task_status(task_id, new_status)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'task_updated',
                    'task_id': task_id,
                    'status': new_status,
                    'task_title': task.title
                }
            )
    
    async def task_updated(self, event):
        await self.send(text_data=json.dumps({
            'type': 'task_updated',
            'task_id': event['task_id'],
            'status': event['status'],
            'task_title': event['task_title']
        }))
    
    @database_sync_to_async
    def update_task_status(self, task_id, new_status):
        task = Task.objects.get(id=task_id)
        task.status = new_status
        task.save()
        return task
