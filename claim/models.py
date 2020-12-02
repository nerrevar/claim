from django.db import models

# Create your models here.
class Group(models.Model):
    group_name = models.CharField(max_length = 80, unique = True, default = 'default')

    def __str__(self):
        return self.group_name

    @property
    def Error_count(self):
        err_count = 0
        for kv in KV.objects.filter(group_name=self.group_name):
            err_count += Claim.objects.filter(KV_name=kv.KV_name).count()
        return err_count

    @property
    def Members(self):
        return KV.objects.filter(group_name = self.group_name)

    def Error_count_filtered(self, start_date, end_date):
        err_count = 0
        for kv in KV.objects.filter(group_name=self.group_name):
            err_count += len(Claim.objects.filter(error_date__range=(start_date, end_date)).filter(KV_name=kv.KV_name))
        return err_count

class Captain(models.Model):
    KV_name = models.ForeignKey(
        'KV',
        on_delete = models.CASCADE,
        to_field = 'KV_name'
    )
    group_name = models.ForeignKey(
        'Group',
        on_delete = models.CASCADE,
        to_field = 'group_name'
    )

    def __str__(self):
        return '{0} -> {1}'.format(self.KV_name, self.group_name)


class Question(models.Model):
    question_number = models.PositiveSmallIntegerField(unique = True)
    question_text = models.CharField(max_length = 100)

    def __str__(self):
        return '{0}. {1}'.format(self.question_number, self.question_text)

    @property
    def Count(self):
        return Claim.objects.filter(question_number=self.question_number).count()

    def Count_filtered(self, start_date, end_date):
        return Claim.objects.filter(error_date__range=(start_date, end_date)).filter(question_number=self.id).count()

    def Count_by_group(self, group_name):
        count = 0
        for kv in Group.objects.get(group_name=group_name).Members:
            count += len(Claim.objects.filter(KV_name=kv.KV_name, question_number=self.id))
        return count

    def Count_by_group_filtered(self, group_name, start_date, end_date):
        count = 0
        for kv in Group.objects.get(group_name=group_name).Members:
            count += len(Claim.objects.filter(error_date__range=(start_date, end_date)).filter(KV_name=kv.KV_name, question_number=self.id))
        return count


class KV(models.Model):
    KV_login = models.CharField(max_length = 30)
    KV_name = models.CharField(max_length = 80, unique = True)
    group_name = models.ForeignKey(
        'Group',
        on_delete = models.CASCADE,
        to_field = 'group_name',
        default = 'default'
    )

    def __str__(self):
        return '{0} - {1}'.format(self.KV_login, self.KV_name)

    @property
    def Error_summary(self):
        return Claim.objects.filter(KV_name=self.KV_name).count()

    @property
    def Error_count_list(self):
        error_count = list()
        for q in Question.objects.order_by('question_number'):
            error_count.append( Claim.objects.filter(question_number=q.id, KV_name=self.KV_name).count() )
        return error_count

    def Error_summary_filtered(self, start_date, end_date):
        return Claim.objects.filter(error_date__range=(start_date, end_date)).filter(KV_name=self.KV_name).count()

    def Error_count_list_filtered(self, start_date, end_date):
        error_count = list()
        for q in Question.objects.order_by('question_number'):
            error_count.append( len( Claim.objects.filter(error_date__range=(start_date, end_date)).filter(question_number=q.id, KV_name=self.KV_name) ) )
        return error_count

    def Error_count_for_question_filtered(self, start_date, end_date, question_number):
        return Claim.objects.filter(error_date__range=(start_date, end_date)).filter(KV_name=self.KV_name).filter(question_number=question_number).count()

    def Group_name(kv_login):
        return KV.objects.filter(KV_login=kv_login).first().group_name.group_name


class Claim(models.Model):
    KV_name = models.ForeignKey('KV', on_delete = models.CASCADE, to_field = 'KV_name')
    question_number = models.ForeignKey('Question', on_delete = models.CASCADE)
    error_date = models.DateField()
    form_id = models.IntegerField(default=100)

    def __str__(self):
        return '{0} -- вопрос №{1} -- {2}'.format(self.error_date, self.question_number, self.KV_name)

    @property
    def Count(self):
        return len(Claim.objects.all())

    def Count_filtered(start_date, end_date):
        return len(Claim.objects.filter(error_date__range=(start_date, end_date)))

    def Count_filtered_date__question_kv(start_date, end_date, question_id, kv_name):
        return len(Claim.objects.filter(KV_name=kv_name, question_number=question_id).filter(error_date__range=(start_date, end_date)))
