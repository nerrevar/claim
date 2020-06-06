from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from .models import Question, KV, Claim, Group

from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def add_error(request):
    template = loader.get_template('claim/add_error.html')
    context = {
        'title': 'Добавить ошибку',
        'kv': KV.objects.order_by('KV_name'),
        'question': Question.objects.order_by('id')
    }
    return HttpResponse(template.render(context, request))

def stat(request):
    template = loader.get_template('claim/stat.html')
    context = {
        'title': 'Статистика',
        'claim_len': len(Claim.objects.all()),
        'Group': Group.objects.order_by('group_name'),
        'KV': KV.objects.order_by('KV_name'),
        'Question': Question.objects.order_by('question_number')
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
