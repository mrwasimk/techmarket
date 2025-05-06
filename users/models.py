from django.contrib.auth.models import User
from django.db import models
from PIL import Image
# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    bank_details_placeholder = models.CharField(max_length=255, blank=True, null=True, help_text="Placeholder only - Do not enter real bank details.")

    def __str__(self): #admin debug
        return f'{self.user.username} Profile'
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # resized uploaded images
        if self.image and hasattr(self.image, 'path') and self.image.name != 'default.jpg':
            try:
                img = Image.open(self.image.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except FileNotFoundError:
                print(f"Warning: Image file not found at {self.image.path} during save.")
            except Exception as e:
                print(f"Error processing image {self.image.path}: {e}")
