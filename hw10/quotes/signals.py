from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Author, Quote
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=Author)
def author_saved(sender, instance, created, **kwargs):
    if created:
        print(f"New author created: {instance.fullname}")

@receiver(post_save, sender=Quote)
def quote_saved(sender, instance, created, **kwargs):
    if created:
        print(f"New quote added: '{instance.text}' by {instance.author.fullname}")

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()