from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import make_password

from datetime import date, timedelta

from .models import Question, KV, Claim, Group, Captain



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


# Auth
def auth(request):
    template = loader.get_template('claim/auth.html')
    return HttpResponse(template.render({}, request))

@csrf_exempt
def log_in(request):
    print(request.POST)
    try:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/')
            return HttpResponse('success')
        return redirect('/auth?error=login')
    except:
        return HttpResponse('not working')
    return redirect('/auth')

def site_logout(request):
    logout(request)
    return redirect('/')

def change_password_view(request):
    template = loader.get_template('claim/change_password.html')
    return HttpResponse(template.render({}, request))

@csrf_exempt
def change_password(request):
    try:
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm = request.POST['confirm']
        print('values')
        if new_password != confirm:
            return redirect('/change_password_view?status=error&error=notmatch')
        user = authenticate(request, username=str(request.user), password=old_password)
        print('user ', user)
        if user is not None:
            print('check password')
            user.set_password(new_password)
            user.save()
            return redirect('/auth')
        else:
            return redirect('/change_password_view?status=error&error=invalid')
    except:
        return HttpResponse('error')


# Add new error page
def add_error(request):
    if not request.user.is_authenticated:
        template = loader.get_template('claim/not_authorized.html')
        return HttpResponse(template.render({}, request))

    template = loader.get_template('claim/add_error.html')
    context = {
        'title': 'Добавить ошибку',
        'kv': KV.objects.order_by('KV_name'),
        'question': Question.objects.order_by('id'),
        'not_show': True
    }
    return HttpResponse(template.render(context, request))


# Main statistics
def stat(request):
    if not request.user.is_authenticated:
        template = loader.get_template('claim/not_authorized.html')
        return HttpResponse(template.render({}, request))

    user_group = 'kv'

    if request.user.groups.filter(name='pret_captain').exists():
        user_group = 'captain'
    if request.user.groups.filter(name='pret_view').exists():
        user_group = 'view'
    if request.user.groups.filter(name='pret_work').exists():
        user_group = 'work'


    template = loader.get_template('claim/stat.html')

    try:
        start_date = date.fromisoformat( request.COOKIES.get('start_date', get_start_month()) )
        end_date = date.fromisoformat( request.COOKIES.get('end_date', get_end_month()) )
    except:
        start_date = get_start_month()
        end_date = get_end_month()

    if user_group not in ('kv', 'captain'):
        count_arr = dict.fromkeys([g.group_name for g in Group.objects.order_by('group_name')])
    else:
        if user_group == 'kv':
            print(request.user)
            count_arr = dict.fromkeys([KV.Group_name(request.user)])
        if user_group == 'captain':
            group_arr = [KV.Group_name(str(request.user))]
            captain_group_name = Captain.objects.filter(
                KV_name=KV.objects.get(KV_login=str(request.user)).KV_name
            ).first().group_name.group_name
            if captain_group_name != KV.Group_name(request.user):
                group_arr.append(captain_group_name)
            count_arr = dict.fromkeys(group_arr)

    for group in Group.objects.order_by('group_name'):
        if group.group_name in count_arr.keys():
            if user_group == 'kv':
                count_arr[group.group_name] = dict.fromkeys([str(request.user)])
            else:
                count_arr[group.group_name] = dict.fromkeys([kv.KV_name for kv in group.Members])
                if user_group == 'captain':
                    captain_group_name = Captain.objects.filter(
                        KV_name=KV.objects.get(KV_login=str(request.user)).KV_name
                    ).first().group_name.group_name
                    if captain_group_name == group.group_name:
                        count_arr[group.group_name]['summary'] = group.Error_count_filtered(start_date, end_date)
                        count_arr[group.group_name]['question'] = list()
                        count_arr[group.group_name]['question'].append('')
                        count_arr[group.group_name]['question'].append('Итого')
                        for q in Question.objects.order_by('question_number'):
                            count_arr[group.group_name]['question'].append(q.Count_by_group_filtered(group.group_name, start_date, end_date))
                        count_arr[group.group_name]['question'].append(group.Error_count_filtered(start_date, end_date))
                else:
                    count_arr[group.group_name]['summary'] = group.Error_count_filtered(start_date, end_date)
                    count_arr[group.group_name]['question'] = list()
                    count_arr[group.group_name]['question'].append('')
                    count_arr[group.group_name]['question'].append('Итого')
                    for q in Question.objects.order_by('question_number'):
                        count_arr[group.group_name]['question'].append(q.Count_by_group_filtered(group.group_name, start_date, end_date))
                    count_arr[group.group_name]['question'].append(group.Error_count_filtered(start_date, end_date))
            for kv in group.Members:
                if user_group in ('kv', 'captain'):
                    if kv.KV_login == str(request.user) or Captain.objects.filter(KV_name=KV.objects.get(KV_login=str(request.user)).KV_name, group_name=group.group_name):
                        count_arr[group.group_name][kv.KV_name] = list()
                        count_arr[group.group_name][kv.KV_name].append(kv.KV_name)
                        count_arr[group.group_name][kv.KV_name].append(kv.KV_login)
                        count_arr[group.group_name][kv.KV_name].extend(kv.Error_count_list_filtered(start_date, end_date))
                        count_arr[group.group_name][kv.KV_name].append(kv.Error_summary_filtered(start_date, end_date))
                else:
                    count_arr[group.group_name][kv.KV_name] = list()
                    count_arr[group.group_name][kv.KV_name].append(kv.KV_name)
                    count_arr[group.group_name][kv.KV_name].append(kv.KV_login)
                    count_arr[group.group_name][kv.KV_name].extend(kv.Error_count_list_filtered(start_date, end_date))
                    count_arr[group.group_name][kv.KV_name].append(kv.Error_summary_filtered(start_date, end_date))

    summary_arr = list()
    summary_arr.append('')
    summary_arr.append('Итого')
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
        'group': user_group
    }
    if user_group in ('pret_view', 'pret_work'):
        context['summary_arr'] = summary_arr
    return HttpResponse(template.render(context, request))


# Statistics for KV
def stat_kv(request):
    if not request.user.is_authenticated:
        template = loader.get_template('claim/not_authorized.html')
        return HttpResponse(template.render({}, request))

    template = loader.get_template('claim/stat_kv.html')

    start_date = date.fromisoformat( request.COOKIES.get('start_date', get_start_month()) )
    end_date = date.fromisoformat( request.COOKIES.get('end_date', get_end_month()) )

    error_count_arr = {kv.KV_name: kv.Error_summary_filtered(start_date, end_date) for kv in KV.objects.all()}
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


# Statistics for questions
def stat_question(request):
    if not request.user.is_authenticated:
        template = loader.get_template('claim/not_authorized.html')
        return HttpResponse(template.render({}, request))

    template = loader.get_template('claim/stat_question.html')

    start_date = date.fromisoformat( request.COOKIES.get('start_date', get_start_month()) )
    end_date = date.fromisoformat( request.COOKIES.get('end_date', get_end_month()) )

    error_count_arr = {'{0}. {1}'.format(q.question_number, q.question_text): q.Count_filtered(start_date, end_date) for q in Question.objects.all()}
    sorted_arr = {k: error_count_arr[k] for k in sorted(error_count_arr, key=error_count_arr.get, reverse=True)}
    context = {
        'title': 'Статистика по вопросам',
        'count_arr': sorted_arr
    }
    return HttpResponse(template.render(context, request))


# For xhr
@csrf_exempt
def write_error(request):
    data = request.POST
    err_date = date.today()
    try:
        kv = KV.objects.get( KV_name=data.get('kv_name') )
        q = Question.objects.get( question_number=data.get('question').split('.')[0] )
        prev = data.get('prev')
        if kv:
            if q:
                if prev == 'true':
                    err_date = date.today().replace(day=1) - timedelta(1)
                c = Claim(
                    KV_name=kv,
                    question_number=q,
                    error_date=err_date
                )
                result = c.save()
                return HttpResponse(result)
        return HttpResponse('except kv_name or question value')
    except:
        return HttpResponse('not working')
