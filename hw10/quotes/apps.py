from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_profiles(sender, **kwargs):
    from django.contrib.auth.models import User
    from quotes.models import Profile

    for user in User.objects.all():
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)

class QuotesConfig(AppConfig):
    name = 'quotes'

    def ready(self):
        import quotes.signals  # Якщо є сигнали
        post_migrate.connect(create_profiles, sender=self)
