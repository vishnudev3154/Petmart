from django.db import models
from django.contrib.auth.models import User


class petdetails(models.Model):
    CATEGORY_CHOICE = [
        ('cat', 'Cat'),
        ('dog', 'Dog'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('fish', 'Fish'),
    ]

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICE)
    name = models.CharField(max_length=100)   # ✅ better than TextField
    description = models.TextField()
    pet_price = models.PositiveIntegerField() # ✅ price cannot be negative
    stock = models.PositiveIntegerField(default=0)  # ✅ NEW FIELD
    pet_image = models.ImageField(upload_to='pet_image/')

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(petdetails, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        return self.product.pet_price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(petdetails, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Pending'
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

from django.utils import timezone

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(petdetails, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.IntegerField()
    order_date = models.DateField(default=timezone.now)
    delivary_date = models.DateField(blank=True, null=True)

