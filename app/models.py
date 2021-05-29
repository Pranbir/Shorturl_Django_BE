from django.db import models


class Urldata(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(blank=False, max_length=1000)
    shortcode = models.CharField( max_length= 20, unique=True)
    added = models.DateTimeField(auto_now_add=True)
    lastupdate = models.DateTimeField(auto_now=True)


class Accessdata(models.Model):
    shortcode = models.ForeignKey(Urldata, on_delete=models.CASCADE)
    referer = models.CharField(blank=True, default="", max_length=200)
    useragent = models.CharField(max_length=200, default="", blank=True)
    ip = models.CharField(max_length=200, default="", blank=True)
    location = models.CharField(max_length=50 , blank=True, default="")



