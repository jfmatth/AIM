from django.db import models

from os.path import basename 

# Create your models here.
class BaseModel(models.Model):
    '''
    Defines some of the base models common fields and functions, mainly save() so we can
    track when the record was updated or created.
    
    Might be worth checking out https://github.com/WiserTogether/django-base-model

    '''
    cdate = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Date Created")     
    mdate = models.DateTimeField(auto_now=True, null=True, verbose_name="Date Modified")
    
    class Meta:
        abstract = True

class Exchange(BaseModel):
    file = models.FileField(upload_to="data/exchange")
    exchange = models.CharField(max_length=100)
    loaded = models.BooleanField()
    
    def __unicode__(self):
        return "%s - %s" % (basename(self.file.path), self.exchange) 

class ExchangePrice(BaseModel):
    exchange = models.ForeignKey(Exchange)
    file = models.FileField(upload_to="data/prices")
    loaded = models.BooleanField()

    def __unicode__(self):
        return "%s " % (basename(self.file.path) )