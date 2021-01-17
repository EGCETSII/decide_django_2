from django.db import models

# Create your models here.

class PeticionCenso(models.Model):
    desc = models.TextField()
    user_id = models.PositiveIntegerField()

    def __str__(self):
        return self.desc