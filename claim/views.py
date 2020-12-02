from datetime import date, timedelta

from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate,logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as Django_group

from .models import Question, KV, Claim, Group, Captain

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
                'number': q.question_number,
                'text': q.question_text,
                'summary': q.Count_filtered(start_date, end_date)
            }
            for q in Question.objects.all()
        ],
        'group': [
            {
                'name': group.group_name,
                'summary': group.Error_count_filtered(start_date, end_date),
                'kv': [
                    {
                        'name': kv.KV_name,
                        'login': kv.KV_login,
                        'summary': kv.Error_summary_filtered(start_date, end_date),
                        'errCountArr': {}
                    }
                    for kv in KV.objects.filter(group_name=group.group_name)
                ]
            }
            for group in Group.objects.all()
        ],
        'claim': [
            {
                'kvName': claim.KV_name.KV_name,
                'questionNumber': claim.question_number.question_number,
                'errorDate': claim.error_date
            }
            for claim in Claim.objects.filter(error_date__range=(start_date, end_date))
        ],
        'captain': [
            {
                'captainName': c.KV_name.KV_name,
                'groupName': c.group_name.group_name
            }
            for c in Captain.objects.all()
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

    error_count_arr = {kv.KV_name: kv.Error_summary_filtered(start_date, end_date) for kv in KV.objects.all()}
    sorted_arr = {k: error_count_arr[k] for k in sorted(error_count_arr, key=error_count_arr.get, reverse=True)}
    count_arr = list()
    for key, value in sorted_arr.items():
        kv = KV.objects.get(KV_name=key)
        count_arr.append([kv.KV_name, kv.KV_login, value])
    return JsonResponse(count_arr, safe=False)

# Statistics for questions
def stat_question(request):
    try:
        start_date = date.fromisoformat( request.GET.get('start_date', get_start_month()) )
        end_date = date.fromisoformat( request.GET.get('end_date', get_end_month()) )
    except:
        start_date = get_start_month()
        end_date = get_end_month()

    error_count_arr = {'{0}. {1}'.format(q.question_number, q.question_text): q.Count_filtered(start_date, end_date) for q in Question.objects.all()}
    sorted_arr = {k: error_count_arr[k] for k in sorted(error_count_arr, key=error_count_arr.get, reverse=True)}
    return JsonResponse(sorted_arr, safe=False)

# Get data for error adding
def get_error_fill_data(request):
    data = {
        'question': [
            {
                'number': q.question_number,
                'text': q.question_text,
            }
            for q in Question.objects.all()
        ],
        'kvList': [
            {
                'name': kv.KV_name,
                'login': kv.KV_login
            }
            for kv in KV.objects.all()
        ]
    }
    return JsonResponse(data, safe=False)

# Get groups
def get_groups(request):
    return JsonResponse([g.group_name for g in Group.objects.all()], safe=False)

# Get array of ligins
def get_login(request):
    return JsonResponse([kv.KV_login for kv in KV.objects.all()], safe=False)

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
        }
        if [r for r in User.objects.get(username=request.session.get('user_login')).groups.all()][0].name != 'pret_work':
            data['name'] = KV.objects.get(KV_login=request.session.get('user_login')).KV_name
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
                'login': request.session.get('user_login'),
                'role': [r for r in User.objects.get(username=request.session.get('user_login')).groups.all()][0].name,
                'project': 'mk',
            }
            if [r for r in User.objects.get(username=request.session.get('user_login')).groups.all()][0].name != 'pret_work':
                data['name'] = KV.objects.get(KV_login=request.session.get('user_login')).KV_name
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
        kv = KV.objects.get( KV_name=data.get('kv_name') )
        q = Question.objects.get( question_number=data.get('question').split('.')[0] )
        prev = data.get('prev')
        print(prev)
        if kv:
            if q:
                if prev == 'on':
                    err_date = date.today().replace(day=1) - timedelta(1)
                c = Claim(
                    KV_name=kv,
                    question_number=q,
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
    data = request.POST # TODO: Parse from JSON
    if (data.get('prev') == 'false'):
        err_date = date.today()
    else:
        err_date = get_end_previous_month()
    claim_arr = data.get('error_list')
    for claim in data.get('error_arr'):
        try:
            Claim.objects.get(
                KV_name=claim.kv,
                question_number=Question.objects.get(question_text=claim.question_text).question_number,
                form_id=claim.form_id
            )
        except:
            tmp_claim = Claim(
                KV_name=KV.objects.get(KV_name=claim.kv),
                question_number=Question.objects.get(question_number=claim.question_number),
                error_date=err_date,
                form_id=claim.form_id
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
        group = Group.objects.get(group_name=request.POST.get('group'))

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
            KV_login=username,
            KV_name=name,
            group_name=Group.objects.get(group_name=group)
        )
        kv.save()
        return HttpResponse(True)
    except:
        return HttpResponse(False)
