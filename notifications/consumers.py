import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        if self.user.is_authenticated:
            self.room_group_name = f'notifications_{self.user.id}'
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            
            # ارسال تعداد اعلان‌های خوانده نشده
            unread_count = await self.get_unread_count()
            await self.send(text_data=json.dumps({
                'type': 'unread_count',
                'count': unread_count
            }))
        else:
            await self.close()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'mark_as_read':
            notification_id = text_data_json.get('notification_id')
            if notification_id:
                await self.mark_notification_as_read(notification_id)
                
                # بروزرسانی تعداد اعلان‌های خوانده نشده
                unread_count = await self.get_unread_count()
                await self.send(text_data=json.dumps({
                    'type': 'unread_count',
                    'count': unread_count
                }))
        
        elif message_type == 'mark_all_as_read':
            await self.mark_all_notifications_as_read()
            
            # بروزرسانی تعداد اعلان‌های خوانده نشده
            unread_count = await self.get_unread_count()
            await self.send(text_data=json.dumps({
                'type': 'unread_count',
                'count': unread_count
            }))
    
    async def send_notification(self, event):
        """ارسال اعلان جدید به کاربر"""
        notification_data = event['notification']
        
        await self.send(text_data=json.dumps({
            'type': 'new_notification',
            'notification': notification_data
        }))
        
        # بروزرسانی تعداد اعلان‌های خوانده نشده
        unread_count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': unread_count
        }))
    
    @database_sync_to_async
    def get_unread_count(self):
        """گرفتن تعداد اعلان‌های خوانده نشده"""
        return Notification.objects.filter(user=self.user, is_read=False).count()
    
    @database_sync_to_async
    def mark_notification_as_read(self, notification_id):
        """علامت‌گذاری اعلان به عنوان خوانده شده"""
        try:
            notification = Notification.objects.get(id=notification_id, user=self.user)
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False
    
    @database_sync_to_async
    def mark_all_notifications_as_read(self):
        """علامت‌گذاری تمام اعلان‌ها به عنوان خوانده شده"""
        Notification.objects.filter(user=self.user, is_read=False).update(
            is_read=True, 
            read_at=timezone.now()
        )

@sync_to_async
def send_notification_to_user(user_id, notification):
    """ارسال اعلان به کاربر خاص از طریق WebSocket"""
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    
    channel_layer = get_channel_layer()
    
    notification_data = {
        'id': notification.id,
        'type': notification.notification_type,
        'title': notification.title,
        'message': notification.message,
        'icon': notification.get_icon(),
        'priority': notification.priority,
        'priority_color': notification.get_priority_color(),
        'created_at': notification.created_at.isoformat(),
        'action_url': notification.action_url or '',
        'is_read': notification.is_read,
    }
    
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user_id}',
        {
            'type': 'send_notification',
            'notification': notification_data
        }
    )
