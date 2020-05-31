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
    question = Question.objects.order_by('question_number')
    claim_arr = Claim.objects.all()
    keys = list()
    # for group in Group.objects.all():
    #     keys.append(group.group_name)
    #     keys.extend([kv.KV_name for kv in KV.objects.all().filter(group_name=group.group_name)])
    count_arr = list()
    # dict.fromkeys(keys)
    index = 0
    count_arr.append(list())
    for group in Group.objects.all():
        # count_arr[group] = list();
        count_arr.append(list())
        index += 1
        count_arr[index].append(group.group_name)
        for kv in KV.objects.filter(group_name=group.group_name):
            kv_err_count += len(Claim.objects.filter(KV_name=kv.KV_name))
        count_arr[index].append(kv_err_count)
        for q in question:
            count_arr[index].append('---')
        count_arr[index].append('---') # Sum column
        kv_err_count = 0
        kv = KV.objects.filter(group_name = group.group_name)
        for k in kv:
            count_arr.append(list())
            index += 1
            # count_arr[k.KV_name] = list()
            count_arr[index].append(k.KV_name)
            count_arr[index].append(k.KV_login)
            for q in question:
                error_count = len(claim_arr.filter(question_number=q.question_number, KV_name=k.KV_name))
                count_arr[index].append(error_count)
            count_arr[index].append(len(claim_arr.filter(KV_name=k.KV_name)))
    # count_arr['sum'] = list()
    count_arr.append(list())
    index += 1
    count_arr[index].append('')
    count_arr[index].append('Итого')
    for q in question:
        count_arr[index].append(len(claim_arr.filter(question_number=q.question_number)))
    context = {
        'title': 'Статистика',
        'kv': kv,
        'question': question,
        'count_arr': count_arr,
        'str_len': len(question) + 3
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
                    KV_name=KV.objects.get(KV_name=data.get('kv_id')),
                    question_number=Question.objects.get(question_number=data.get('q_id'))
                )
                result = c.save()
                return HttpResponse(result)
    return HttpResponse('false')
