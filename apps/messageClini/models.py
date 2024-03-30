from django.contrib.auth.models import User
from django.db import models
from apps.nutritionist.models import Nutritionist

class MessageClini(models.Model):
    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE, related_name='messageClini_nutritionist', null=False, blank=False)
    message = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = "MessageClini"
        verbose_name_plural = "MessageClinis"

    def __str__(self):
        return self.message