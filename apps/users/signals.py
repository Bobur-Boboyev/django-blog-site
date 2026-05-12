from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("Profile succesfully created!")
    else:
        instance.profile.save()
        print("Profile succesfully updated!")

@receiver(pre_delete, sender=Profile)
def delete_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.delete()
        print("profile deleted")
    except Profile.DoesNotExist():
        pass