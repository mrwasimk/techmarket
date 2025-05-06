from django import forms
from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image

#Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

#Product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='product_pics', null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    #ForeignKey
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    def __str__(self):
        return self.name
    #Image resizing
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            try:
                img = Image.open(self.image.path)
                max_width = 800
                max_height = 800
                if img.height > max_height or img.width > max_width:
                    output_size = (max_width, max_height)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except Exception as e:
                print(f"Error resizing image {self.image.path}: {e}")