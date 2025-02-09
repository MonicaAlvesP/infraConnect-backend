from django.db import models
from django.conf import settings
import uuid


class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4().hex
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.key
