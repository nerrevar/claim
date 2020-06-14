from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from .models import Question, KV, Claim, Group

from django.views.decorators.csrf import csrf_exempt

from datetime import date, timedelta


def get_start_month():
    tmp_date = date.today()
    tmp_date = tmp_date.replace(day=1)
    return tmp_date.isoformat()

def get_end_month():
    tmp_date = date.today()
    tmp_date = tmp_date.replace(day=1)
    tmp_date = tmp_date.replace(month = tmp_date.month + 1)
    tmp_date -= timedelta(1)
    return tmp_date.isoformat()


# Create your views here.
def add_error(request):
    template = loader.get_template('claim/add_error.html')
    context = {
        'title': 'Добавить ошибку',
        'kv': KV.objects.order_by('KV_name'),
        'question': Question.objects.order_by('id'),
        'not_show': True
    }
    return HttpResponse(template.render(context, request))

def stat(request):
    template = loader.get_template('claim/stat.html')

    print(request.COOKIES.items())

    start_date = date.fromisoformat( request.COOKIES.get('start_date', get_start_month()) )
    end_date = date.fromisoformat( request.COOKIES.get('end_date', get_end_month()) )

    print('start_date: ', start_date)
    print('end_date: ', end_date)

    count_arr = dict.fromkeys([g.group_name for g in Group.objects.order_by('group_name')])
    for group in Group.objects.order_by('group_name'):
        count_arr[group.group_name] = dict.fromkeys([group.Members])
        count_arr[group.group_name]['summary'] = group.Error_count_filtered(start_date, end_date)
        count_arr[group.group_name]['question'] = list()
        count_arr[group.group_name]['question'].append('')
        count_arr[group.group_name]['question'].append('Итого')
        for q in Question.objects.order_by('question_number'):
            count_arr[group.group_name]['question'].append(q.Count_by_group_filtered(group.group_name, start_date, end_date))
        count_arr[group.group_name]['question'].append(group.Error_count_filtered(start_date, end_date))
        for kv in group.Members:
            count_arr[group.group_name][kv.KV_name] = list()
            count_arr[group.group_name][kv.KV_name].append(kv.KV_name)
            count_arr[group.group_name][kv.KV_name].append(kv.KV_login)
            count_arr[group.group_name][kv.KV_name].extend(kv.Error_count_list_filtered(start_date, end_date))
            count_arr[group.group_name][kv.KV_name].append(kv.Error_summary_filtered(start_date, end_date))

    summary_arr = list()
    for q in Question.objects.order_by('question_number'):
        summary_arr.append(q.Count_filtered(start_date, end_date))
    summary_arr.append(Claim.Count_filtered(start_date, end_date))

    context = {
        'title': 'Статистика',
        'claim_len': Claim.objects.filter(
                error_date__gte = start_date
            ).filter(
                error_date__lte = end_date
            ).count(),
        'Question': Question.objects.order_by('question_number'),
        'count_arr': count_arr,
        'summary_arr': summary_arr
    }
    return HttpResponse(template.render(context, request))

def stat_kv(request):
    template = loader.get_template('claim/stat_kv.html')
    error_count_arr = {kv.KV_name: kv.Error_summary for kv in KV.objects.all()}
    sorted_arr = {k: error_count_arr[k] for k in sorted(error_count_arr, key=error_count_arr.get, reverse=True)}
    count_arr = list()
    for key, value in sorted_arr.items():
        kv = KV.objects.get(KV_name=key)
        count_arr.append([kv.KV_name, kv.KV_login, value])
    context = {
        'title': 'Статистика по КВ',
        'count_arr': count_arr
    }
    return HttpResponse(template.render(context, request))

def stat_question(request):
    template = loader.get_template('claim/stat_question.html')
    error_count_arr = {'{0}. {1}'.format(q.question_number, q.question_text): q.Count for q in Question.objects.all()}
    sorted_arr = {k: error_count_arr[k] for k in sorted(error_count_arr, key=error_count_arr.get, reverse=True)}
    context = {
        'title': 'Статистика по вопросам',
        'count_arr': sorted_arr
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def write_error(request):
    data = request.POST
    try:
        kv = KV.objects.get( KV_name=data.get('kv_name') )
        q = Question.objects.get( question_number=data.get('question').split('.')[0] )
        if kv:
            if q:
                c = Claim(
                    KV_name=kv,
                    question_number=q
                )
                result = c.save()
                return HttpResponse(result)
        return HttpResponse('except kv or q')
    except:
        return HttpResponse('false')
