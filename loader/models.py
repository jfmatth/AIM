from django.db import models

# Create your models here.

class Loaddate(models.Model):
    date = models.DateField()
    loaded = models.BooleanField()
    
    
