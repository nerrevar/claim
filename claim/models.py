from django.db import models

# Create your models here.
class Question(models.Model):
    question_number = models.PositiveSmallIntegerField()
    question_text = models.CharField(max_length = 100)

class KV(models.Model):
    KV_login = models.CharField(max_length = 30)
    KV_name = models.CharField(max_length = 80)

class Claim(models.Model):
    KV_name = models.ForeignKey('KV', on_delete = models.CASCADE)
    question_number = models.ForeignKey('Question', on_delete = models.CASCADE)
    error_date = models.DateField(auto_now=True)
