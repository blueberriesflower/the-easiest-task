from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    """
    Модель для комнаты чата.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name="Название комнаты")
    users = models.ManyToManyField(User, related_name='chatrooms', verbose_name="Участники")
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admin_of', verbose_name="Администратор") # Admin of the chat

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Комната чата"
        verbose_name_plural = "Комнаты чата"


class Message(models.Model):
    """
    Модель для сообщений.
    """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', verbose_name="Комната")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name="Пользователь")
    content = models.TextField(verbose_name="Содержание")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")
    file = models.FileField(upload_to='chat_files/', blank=True, null=True, verbose_name="Файл")  # For media files
    edited = models.BooleanField(default=False, verbose_name="Отредактировано")
    deleted = models.BooleanField(default=False, verbose_name="Удалено")

    def __str__(self):
        return f"Сообщение от {self.user.username} в {self.room.name}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

class MessageHistory(models.Model):
    """
    Модель для истории сообщений.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    action = models.CharField(max_length=255, verbose_name="Действие") # e.g., "created", "edited", "deleted"
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь, выполнивший действие") # User who performed the action
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время действия")
    previous_content = models.TextField(blank=True, null=True, verbose_name="Предыдущее содержание") # Store the content before changes

    def __str__(self):
        return f"История сообщения {self.message.id}: {self.action} by {self.user.username if self.user else 'System'}"

    class Meta:
        verbose_name = "История сообщения"
        verbose_name_plural = "История сообщений"