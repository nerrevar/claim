from django.db import models

# Create your models here.
class Group(models.Model):
    group_name = models.CharField(max_length = 80, unique = True, default = 'default')

    @property
    def Error_count(self):
        err_count = 0
        for kv in KV.objects.filter(group_name=self.group_name):
            err_count += len(Claim.objects.filter(KV_name=kv.KV_name))
        return err_count

class Question(models.Model):
    question_number = models.PositiveSmallIntegerField(unique = True)
    question_text = models.CharField(max_length = 100)

    @property
    def Count(self):
        return len(Claim.objects.filter(question_number=self.question_number))

class KV(models.Model):
    KV_login = models.CharField(max_length = 30)
    KV_name = models.CharField(max_length = 80, unique = True)
    group_name = models.ForeignKey('Group', on_delete = models.CASCADE, to_field = 'group_name', default = 'default')

    @property
    def Error_summary(self):
        return len(Claim.objects.filter(KV_name=self.KV_name))

    @property
    def Error_count_list(self):
        error_count = list()
        for q in Question.objects.order_by('question_number'):
            error_count.append(len(Claim.objects.filter(question_number=q.question_number, KV_name=self.KV_name)))
        return error_count

class Claim(models.Model):
    KV_name = models.ForeignKey('KV', on_delete = models.CASCADE, to_field = 'KV_name')
    question_number = models.ForeignKey('Question', on_delete = models.CASCADE, to_field = 'question_number')
    error_date = models.DateField(auto_now=True)
