from datetime import date, timedelta

import json

from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate,logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as Django_group

from .models import Question, KV, Claim, Group

# Internal use
def get_start_month():
    tmp_date = date.today()
    tmp_date = tmp_date.replace(day=1)
    return tmp_date.isoformat()

# Internal use
def get_end_month():
    tmp_date = date.today()
    tmp_date = tmp_date.replace(day=1)
    if tmp_date.month <= 11:
      tmp_date = tmp_date.replace(month = tmp_date.month + 1)
    else:
      tmp_date = tmp_date.replace(month = 1)
      tmp_date = tmp_date.replace(year = tmp_date.year + 1)
    tmp_date -= timedelta(1)
    return tmp_date.isoformat()

# Internal use
def get_end_previous_month():
    tmp_date = date.today()
    tmp_date = tmp_date.replace(day=1)
    tmp_date -= timedelta(1)
    return tmp_date

# Return main template
def index(request):
    template = loader.get_template('claim/index.html')
    return HttpResponse(template.render({}, request))

# Main statistics
def stat(request):
    try:
        start_date = date.fromisoformat( request.GET.get('start_date', get_start_month()) )
        end_date = date.fromisoformat( request.GET.get('end_date', get_end_month()) )
    except:
        start_date = get_start_month()
        end_date = get_end_month()

    response = {
        'question': [
            {
                'number': q.number,
                'text': q.text,
                'summary': q.Count(start_date, end_date)
            }
            for q in Question.objects.all()
        ],
        'group': [
            {
                'name': group.name,
                'summary': group.Count(start_date, end_date),
                'kv': [
                    {
                        'name': kv.name,
                        'login': kv.login,
                        'summary': kv.Count(start_date, end_date),
                        'errCountArr': {}
                    }
                    for kv in group.Members()
                ]
            }
            for group in Group.objects.all()
        ],
        'claim': [
            {
                'kvName': claim.kv.name,
                'questionNumber': claim.question.number,
                'errorDate': claim.error_date
            }
            for claim in Claim.ByDate(start_date, end_date)
        ]
    }

    return JsonResponse(response)

# Statistics for KV
def stat_kv(request):
    try:
        start_date = date.fromisoformat( request.GET.get('start_date', get_start_month()) )
        end_date = date.fromisoformat( request.GET.get('end_date', get_end_month()) )
    except:
        start_date = get_start_month()
        end_date = get_end_month()

    error_count_arr = {kv.name: kv.Count(start_date, end_date) for kv in KV.objects.all()}
    sorted_arr = {k: error_count_arr[k] for k in sorted(error_count_arr, key=error_count_arr.get, reverse=True)}
    count_arr = list()
    for key, value in sorted_arr.items():
        kv = KV.objects.get(name=key)
        count_arr.append([kv.name, kv.login, value])
    return JsonResponse(count_arr, safe=False)

# Statistics for questions
def stat_question(request):
    try:
        start_date = date.fromisoformat( request.GET.get('start_date', get_start_month()) )
        end_date = date.fromisoformat( request.GET.get('end_date', get_end_month()) )
    except:
        start_date = get_start_month()
        end_date = get_end_month()

    error_count_arr = {'{0}. {1}'.format(q.number, q.text): q.Count(start_date, end_date) for q in Question.objects.all()}
    sorted_arr = {k: error_count_arr[k] for k in sorted(error_count_arr, key=error_count_arr.get, reverse=True)}
    return JsonResponse(sorted_arr, safe=False)

# Returns claim's numbers
def get_numbers(request):
    try:
        start_date = date.fromisoformat( request.GET.get('start_date', get_start_month()) )
        end_date = date.fromisoformat( request.GET.get('end_date', get_end_month()) )
    except:
        start_date = get_start_month()
        end_date = get_end_month()

    login = request.GET.get('login')
    resp = [
        {
            'number': c.form_id,
            'question': c.question.text
        }
        for c in Claim.ByKV(start_date, end_date, KV.objects.get(login=login))
    ]
    if (len(resp) == 0):
      return JsonResponse({'status': 'zero'})
    else:
      return JsonResponse(resp, safe=False)

# Get data for error adding
def get_error_fill_data(request):
    data = {
        'question': [
            {
                'number': q.number,
                'text': q.text,
            }
            for q in Question.objects.all()
        ],
        'kvList': [
            {
                'name': kv.name,
                'login': kv.login
            }
            for kv in KV.objects.all()
        ]
    }
    return JsonResponse(data, safe=False)

# Get groups
def get_groups(request):
    return JsonResponse([g.name for g in Group.objects.all()], safe=False)

# Get array of ligins
def get_login(request):
    return JsonResponse([kv.login for kv in KV.objects.all()], safe=False)

# For xhr (post)
# Login
@csrf_exempt
def login(request):
    if request.session.get('user_login', False):
        data = {
            'status': 'True',
            'login': request.session.get('user_login'),
            'role': [r for r in User.objects.get(username=request.session.get('user_login')).groups.all()][0].name,
            'project': 'mk',
            'group_name': KV.objects.get(login=request.session.get('user_login')).group.name
        }
        if [r for r in User.objects.get(username=request.session.get('user_login')).groups.all()][0].name != 'pret_work':
            data['name'] = KV.objects.get(login=request.session.get('user_login')).name
        return JsonResponse(data, safe=False)

    try:
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)

        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({'status': 'Error', 'error': 'Invalid username or password'})
        else:
            request.session['user_login'] = username

            data = {
                'status': 'True',
                'login': username,
                'role': [r for r in User.objects.get(username=username).groups.all()][0].name,
                'project': 'mk',
                'group_name': KV.objects.get(login=username).group.name
            }
            if [r for r in User.objects.get(username=username).groups.all()][0].name != 'pret_work':
                data['name'] = KV.objects.get(login=username).name
            return JsonResponse(data, safe=False)
    except:
        return JsonResponse({ 'status': False })

# Logout
def site_logout(request):
    logout(request)
    return HttpResponse(True)

# Add error
@csrf_exempt
def write_error(request):
    data = request.POST
    if (data.get('prev') == 'false'):
      err_date = date.today()
    else:
      err_date = get_end_previous_month()
    try:
        kv = KV.objects.get(name=data.get('kv_name'))
        q = Question.objects.get(number=data.get('question').split('.')[0])
        prev = data.get('prev')
        print(prev)
        if kv:
            if q:
                c = Claim(
                    kv=kv,
                    question=q,
                    error_date=err_date
                )
                result = c.save()
                return HttpResponse(True)
        return HttpResponse('Params')
    except:
        return HttpResponse(False)

# Add error multiple
@csrf_exempt
def write_error_multiple(request):
    data = json.loads(request.body)
    if (data.get('prev') == True):
        err_date = get_end_previous_month()
    else:
        err_date = date.today()
    claim_arr = data.get('error_list')
    for claim in claim_arr:
        try:
            Claim.objects.get(
                kv=KV.objects.get(login=claim.get('login')),
                question=Question.objects.get(text=claim.get('question_text')),
                form_id=claim.get('form_id')
            )
        except:
            tmp_claim = Claim(
                kv=KV.objects.get(login=claim.get('login')),
                question=Question.objects.get(text=claim.get('question_text')),
                error_date=err_date,
                form_id=claim.get('form_id')
            )
            tmp_claim.save()
    return HttpResponse(True)

# Add user
@csrf_exempt
def user_add(request):
    try:
        name = request.POST.get('name')
        username = request.POST.get('username')
        django_group = request.POST.get('role')
        group = Group.objects.get(name=request.POST.get('group'))

        if (len(User.objects.filter(username=username)) > 0):
            return HttpResponse('User exist')

        user = User(
            username=username,
            password=make_password(2 * username),
            is_active=True
        )
        user.save()
        user.groups.add(Django_group.objects.get(name=django_group))
        kv = KV(
            login=username,
            name=name,
            group=Group.objects.get(name=group)
        )
        kv.save()
        return HttpResponse(True)
    except:
        return HttpResponse(False)
