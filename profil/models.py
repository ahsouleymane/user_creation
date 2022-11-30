from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Account(models.Model):

    util = models.OneToOneField(User, on_delete=models.CASCADE)

    profession = models.CharField(max_length=50, null=True)
    genre = models.CharField(max_length=50, choices=[('Masculin', 'Masculin'),('Féminin', 'Féminin')])

    def __str__(self):
        return self.util.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(util=instance)

