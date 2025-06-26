from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from .models import LoginHistory, UserProfile


@receiver(user_logged_in)
def login_success(sender, request, user, **kwargs):
    # Create a LoginHistory instance
    LoginHistory.objects.create(user=user, ip_address=request.META.get('REMOTE_ADDR'), user_agent=request.META.get('HTTP_USER_AGENT'))

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()