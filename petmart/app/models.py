from django.db import models
from django.contrib.auth.models import User


class petdetails(models.Model):
    CATEGORY_CHOICE=[
        # ('database value','form value')
        ('cat','cat'),
        ('dog','dog'),
        ('bird','bird'),
        ('rabbit','rabbit'),
        ('fish','fish')
]
    category=models.CharField(max_length=10,choices=CATEGORY_CHOICE)
    name=models.TextField()
    description=models.TextField()
    pet_price=models.IntegerField()
    pet_image=models.ImageField(upload_to='pet_image/')
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(petdetails, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
# WISHLIST MODEL
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(petdetails, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
