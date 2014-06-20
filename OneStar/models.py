from django.db import models

# Create your models here.

class OneStarAuth(models.Model):
    class Meta:
        permissions = (
            ("can_view", "Can view this page"),
        )