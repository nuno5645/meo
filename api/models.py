from django.db import models

class MyModel(models.Model):
    
    name = models.CharField(max_length=100)
    points = models.IntegerField()
    url = models.URLField()
    available = models.BooleanField()
    image_url = models.URLField()
    link_url = models.URLField()
    description = models.TextField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name