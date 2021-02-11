from django.db import models


class Psychotherapist(models.Model):
    airtable_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='media', blank=True, null=True)
    methods = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'psychotherapist'
        verbose_name = 'психотерапевт'
        verbose_name_plural = 'психотерапевты'

    def __str__(self):
        return self.name


class PsychotherapistRawData(models.Model):
    data = models.TextField()
    creation_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'psychotherapist_raw_data'

    def __str__(self):
        return f'Бэкап от {self.creation_time}'
