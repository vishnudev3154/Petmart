from django.db import models

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
    