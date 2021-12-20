from django.db import models

class Medicine(models.Model):

    medicine_id = models.AutoField(primary_key = True)
    common_name = models.CharField(max_length = 100)
    scientific_name = models.CharField(max_length = 100)
    category = models.CharField(max_length = 100)
