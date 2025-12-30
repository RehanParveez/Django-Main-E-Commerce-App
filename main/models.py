from django.db import models
from DjangoMainECommerce.models import BaseModel

# Create your models here.
class ContactUs(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField()
    subject = models.CharField(max_length=170)
    message = models.TextField()
    
    def __str__(self):
        return f"{self.name}"
    