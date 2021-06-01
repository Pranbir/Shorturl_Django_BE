from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Urldata(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(blank=False, max_length=1000)
    shortcode = models.CharField( max_length= 20, unique=True)
    added = models.DateTimeField(auto_now_add=True)
    lastupdate = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "{} .   | {}   |   {}".format(self.id, self.url , self.shortcode )
    
    def save(self, *args, **kwargs):
        super(Urldata, self).save(*args, **kwargs)




class Accessdata(models.Model):
    shortcode = models.ForeignKey(Urldata, on_delete=models.CASCADE)
    referer = models.CharField(blank=True, default="", max_length=200)
    useragent = models.CharField(max_length=200, default="", blank=True)
    ip = models.CharField(max_length=200, default="", blank=True)
    location = models.CharField(max_length=50 , blank=True, default="")



@receiver(pre_save, sender=Urldata)
def update_short_url(sender, instance, *args, **kwargs):
    shortcode_extra=""
    i=1
    while True:
        if sender.objects.filter(shortcode=instance.shortcode+shortcode_extra):
            i+=1
            shortcode_extra = str(i)
        else:
            break
    instance.shortcode += shortcode_extra