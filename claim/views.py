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
    count_arr = dict.fromkeys([group.group_name for group in Group.objects.all()])
    for group in Group.objects.all():
        count_arr[group.group_name] = dict.fromkeys([kv.KV_name for kv in KV.objects.all().filter(group_name=group.group_name)])
        kv_err_count = 0
        for kv in KV.objects.filter(group_name=group.group_name):
            kv_err_count += len(Claim.objects.filter(KV_name=kv.KV_name))
        count_arr[group.group_name]['error_count'] = kv_err_count # Group error count

        kv = KV.objects.filter(group_name = group.group_name) # KV from current group
        for k in kv:
            count_arr[group.group_name][k.KV_name] = list()
            count_arr[group.group_name][k.KV_name].append(k.KV_name)
            count_arr[group.group_name][k.KV_name].append(k.KV_login)
            for q in question:
                error_count = len(claim_arr.filter(question_number=q.question_number, KV_name=k.KV_name))
                count_arr[group.group_name][k.KV_name].append(error_count) # Add error count for each question to KV's list
            count_arr[group.group_name][k.KV_name].append(len(claim_arr.filter(KV_name=k.KV_name))) # Add summary error count

    summary_arr = list()
    summary_arr.append('')
    summary_arr.append('Итого')
    for q in question:
        summary_arr.append(len(claim_arr.filter(question_number=q.question_number)))
    context = {
        'title': 'Статистика',
        'claim_len': len(Claim.objects.all()),
        'Group': Group.objects.all(),
        'KV': KV.objects.all(),
        'Question': Question.objects.order_by('question_number')
    }
    print(count_arr)
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
