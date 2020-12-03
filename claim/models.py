from django.db import models

class KV(models.Model):
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=100, unique=True)
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '{0} -- {1}'.format(self.login, self.name)

    def Count(self, start_date, end_date):
        return len(Claim.ByKV(start_date, end_date, self))

class Question(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    text = models.CharField(max_length=500)

    def __str__(self):
        return '{0}.  {1}'.format(self.number, self.text)

    def Count(self, start_date, end_date):
        return len(Claim.ByQuestion(start_date, end_date, self))

class Claim(models.Model):
    kv = models.ForeignKey(
        'KV',
        on_delete = models.CASCADE
    )
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )
    error_date = models.DateField()
    form_id = models.IntegerField()

    def __str__(self):
        return '{0} -- {1} ({2}) -- {3}. {4}'.format(
            self.error_date,
            self.kv.login,
            self.kv.name,
            self.question.number,
            self.question.text
        )

    def ByDate(start_date, end_date):
        return Claim.objects.filter(error_date__range=(start_date, end_date))

    def ByKV(start_date, end_date, kv):
        return Claim.ByDate(start_date, end_date).filter(kv=kv)

    def ByQuestion(start_date, end_date, question):
        return Claim.ByDate(start_date, end_date).filter(question=question)

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def Members(self):
        return KV.objects.filter(group=self)

    def Count(self, start_date, end_date):
        err_count = 0
        for kv in self.Members():
            err_count += len(Claim.ByKV(start_date, end_date, kv))
        return err_count
