from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message

@receiver(post_save, sender=Message)
def notify_clients(sender, instance, **kwargs):
    # WebSocket orqali foydalanuvchilarga xabar yuborish mexanizmini bu yerga qo'shing
    pass
