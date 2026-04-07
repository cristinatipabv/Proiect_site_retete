# https://docs.djangoproject.com/en/6.0/topics/signals/

import os
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import Recipe


@receiver(pre_save, sender=Recipe)
def my_signal_pre_save(sender, instance: Recipe, **kwargs):

    print("Saving recipe!.")

@receiver(pre_delete, sender=Recipe)
def cleanup_image(sender, instance: Recipe, **kwargs):

    if instance.image is not None:
        try:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
        except ValueError as e:

            pass

