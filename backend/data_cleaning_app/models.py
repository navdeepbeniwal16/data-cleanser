from django.db import models

# Create your models here.
class DataFile(models.Model):
    file = models.FileField()
    uploaded_on = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.uploaded_on.date()
