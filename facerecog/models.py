from django.db import models

def folder(instance, filename):
    return "%s/%s" %(instance.name, filename)

class User(models.Model):
    name = models.CharField(max_length=20)
    front = models.ImageField(upload_to=folder)
    top = models.ImageField(upload_to=folder)
    right = models.ImageField(upload_to=folder)
    left = models.ImageField(upload_to=folder)
    bottom = models.ImageField(upload_to=folder)
    
    def __str__(self):
        return "%s. %s" %(self.userid, self.name)