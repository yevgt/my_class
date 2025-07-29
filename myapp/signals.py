from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task, TaskStatusChange

@receiver(post_save, sender=Task)
def send_task_status_notification(sender, instance, created, **kwargs):
   if not created and instance.status_changed:
       # Проверяем, было ли изменение статуса
       last_status = TaskStatusChange.objects.filter(task=instance).order_by('-changed_at').first()
       if not last_status or last_status.status != instance.status:
           TaskStatusChange.objects.create(task=instance, status=instance.status)
           subject = f'Task "{instance.title}" Status Update'
           message = f'The status of your task "{instance.title}" has been changed to {instance.status}.'
           from_email = 'from@example.com'
           recipient_list = [instance.owner.email]
           send_mail(subject, message, from_email, recipient_list, fail_silently=True)
       instance.status_changed = False
       instance.save(update_fields=['status_changed'])

@receiver(pre_delete, sender=Task)
def send_task_deletion_notification(sender, instance, **kwargs):
   subject = f'Task "{instance.title}" Deleted'
   message = f'Your task "{instance.title}" has been deleted.'
   from_email = 'from@example.com'
   recipient_list = [instance.owner.email]
   send_mail(subject, message, from_email, recipient_list, fail_silently=True)