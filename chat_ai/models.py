from django.db import models
from users.models  import User

# Create your models here.
class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.JSONField(default=list)
    created_at = models. DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'ChatSession {self.id}- {self.user.username}'