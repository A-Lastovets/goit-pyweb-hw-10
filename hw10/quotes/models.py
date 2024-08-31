from djongo import models as mongo_models
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
import uuid

class ObjectIdField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 24
        kwargs['primary_key'] = True
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) in [None, '']:
            # Generate a new unique ID
            new_id = uuid.uuid4().hex[:24]
            setattr(model_instance, self.attname, new_id)
        return super().pre_save(model_instance, add)

class Author(models.Model):
    id = ObjectIdField()
    fullname = models.TextField()
    born_date = models.DateField(null=True, blank=True)  # Використовуйте DateField замість DateTimeField
    born_location = models.CharField(max_length=100, default="Unknown")
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Не перетворюйте born_date в формат рядка тут
        super().save(*args, **kwargs)

    def __str__(self):
        return self.fullname
    
class Quote(mongo_models.Model):
    text = mongo_models.TextField()
    author = mongo_models.ForeignKey(Author, on_delete=mongo_models.CASCADE)

    def __str__(self):
        return self.text

# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='cat.jpg', upload_to='profile_images')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Resizing images
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Ensure the Profile instance is saved before processing the image

        # Check if an avatar image is being uploaded
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 250 or img.width > 250:
                new_img = (250, 250)
                img.thumbnail(new_img)
                img.save(self.avatar.path)
