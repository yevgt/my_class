from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Task



# @receiver - это декоратор для подключения функции к сигналу
# Первый аргумент - сам сигнал (post_save)
# sender=Task - указывает, что мы слушаем сигнал только от модели Task
@receiver(pre_save, sender=Task)
def task_status_change_notification(sender, instance, **kwargs):
    if not instance.pk:
        # Новая задача — уведомлять не нужно
        return

    try:
        old_instance = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    old_status = old_instance.status
    new_status = instance.status

    # Проверяем, что статус изменился
    if old_status != new_status:
        # Используем поле instance._status_notified для предотвращения повторной рассылки
        # Отправляем почту только если ещё не отправляли по этому статусу (на основе свойства модели или кеша)

        notified_attr = '_notified_for_status'
        previously_notified_status = getattr(instance, notified_attr, None)

        if previously_notified_status == new_status:
            # Уже отправляли уведомление для этого статуса, пропускаем
            return

        # Формируем тему и тело письма (пример)
        subject = f"Статус задачи изменён на '{new_status}'"
        message = f"Здравствуйте, задача '{instance.title}' была переведена в статус '{new_status}'."

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.author.email],
            fail_silently=False,
        )

        # Помечаем, что уведомление для этого статуса отправлено
        setattr(instance, notified_attr, new_status)
