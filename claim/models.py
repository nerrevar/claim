from django.db import models

# Create your models here.
class Group(models.Model):
    group_name = models.CharField(max_length = 80, unique = True, default = 'default')

class Question(models.Model):
    question_number = models.PositiveSmallIntegerField(unique = True)
    question_text = models.CharField(max_length = 100)

class KV(models.Model):
    KV_login = models.CharField(max_length = 30)
    KV_name = models.CharField(max_length = 80, unique = True)
    group_name = models.ForeignKey('Group', on_delete = models.CASCADE, to_field = 'group_name', default = 'default')

class Claim(models.Model):
    KV_name = models.ForeignKey('KV', on_delete = models.CASCADE, to_field = 'KV_name')
    question_number = models.ForeignKey('Question', on_delete = models.CASCADE, to_field = 'question_number')
    error_date = models.DateField(auto_now=True)
