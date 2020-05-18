from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from .models import Question, KV, Claim

from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def add_error(request):
    template = loader.get_template('claim/add_error.html')
    context = {
        'title': 'Добавить ошибку',
        'kv': KV.objects.order_by('KV_login'),
        'question': Question.objects.order_by('id')
    }
    return HttpResponse(template.render(context, request))

def stat(request):
    template = loader.get_template('claim/stat.html')
    kv = KV.objects.order_by('KV_login')
    kv_list = list();
    for k in kv:
        kv_list.append(k.KV_name)
    question = Question.objects.order_by('question_number')
    claim_arr = Claim.objects.all()
    count_arr = dict.fromkeys(kv_list)
    for k in kv:
        count_arr[k.KV_name] = list()
        count_arr[k.KV_name].append(k.KV_name)
        count_arr[k.KV_name].append(k.KV_login)
        for q in question:
            error_count = len(claim_arr.filter(question_number=q.id, KV_name=k.id))
            count_arr[k.KV_name].append(error_count)
        count_arr[k.KV_name].append(len(claim_arr.filter(KV_name=k.id)))
    count_arr['sum'] = list()
    count_arr['sum'].append('')
    count_arr['sum'].append('Итого')
    for q in question:
        count_arr['sum'].append(len(claim_arr.filter(question_number=q.id)))
    context = {
        'title': 'Статистика',
        'kv': kv,
        'question': question,
        'count_arr': count_arr
    }
    return HttpResponse(template.render(context, request))

# def stat_kv(request):
#     template = loader.get_template('claim/stat_kv.html')
#     claim_arr = Claim.objects.all()
#     kv = KV.objects.order_by('KV_login')
#     kv_list = list();
#     for k in kv:
#         kv_list.append(k.KV_name)
#     count_arr = dict.fromkeys(kv_list)
#     for k in kv:
#         count_arr[k.KV_name] = len(claim_arr.filter(KV_name=k.id))
#     sorted_arr = {k: v for k, v in sorted(count_arr.items(), key=lambda item: item[1])}
#     context = {
#         'title': 'Статистика КВ',
#         'count_arr': sorted_arr
#     }
#     return HttpResponse(template.render(context, request))

@csrf_exempt
def write_error(request):
    data = request.POST
    if data.get('kv_id') and data.get('q_id'):
        if data.get('kv_id') != 'None':
            if data.get('q_id') != 'None':
                c = Claim(
                    KV_name=KV.objects.get(id=data.get('kv_id')),
                    question_number=Question.objects.get(id=data.get('q_id'))
                )
                result = c.save()
                return HttpResponse(result)
    return HttpResponse('false')
