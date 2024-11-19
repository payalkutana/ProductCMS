from django.db import models

# Create your models here.
class product(models.Model):
    name = models.CharField(max_length=50,blank=False)
    image = models.ImageField(upload_to='product_images/',blank=True)
    price = models.IntegerField(blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)