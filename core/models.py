from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

if settings.VULNERABLE == False:
   class Comment(models.Model):
       base_username = models.CharField(max_length=32)
       user_comment = models.TextField(max_length=32)
       user_count = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(3)])
       def __str__(self):
           return self.user_count
