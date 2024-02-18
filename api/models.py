from django.db import models

class Product(models.Model):
    
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)
    url = models.URLField(default='')
    available = models.BooleanField( default=True)
    image_url = models.URLField(default='')
    link_url = models.URLField(default='')
    description = models.TextField(default='')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    points = models.IntegerField(default=0)
    products = models.ManyToManyField(Product, blank=True)
    
    def __str__(self):
        return self.name