from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Confession, ConfessionReport, ConfessionRequest
from .forms import ConfessionForm, ConfessionReportForm
import json
from django.http import JsonResponse

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    
def index(request):

    if not request.user.is_authenticated:
        context = {}
        return render(request, 'landing.html', context)
    confession_list = Confession.objects.all()
    confession_list = confession_list.filter(visibility = True).order_by("-timestamp")
    context = {'confessions':confession_list, 'is_moderator':request.user.groups.filter(name='moderators').exists()}
    return render(request, 'index.html', context)

def create_confession(request):
    
    if not request.user.is_authenticated:
        return redirect('index')

    form = ConfessionForm(request.POST or None)
    if form.is_valid() and request.user.is_authenticated:
        
        new_confession = form.save(commit=False)
        new_confession.ip_address = get_client_ip(request)
        new_confession.save()
        return redirect('index')

    context = {'form':form, 'is_moderator':request.user.groups.filter(name='moderators').exists()}

    return render(request, "create_confession.html", context)

def logout(request):
    return redirect('/accounts/logout')

def login(request):
    return redirect('/accounts/google/login/?process=login')

def pending(request):
    
    if not request.user.is_authenticated:
        context = {}
        return render(request, 'landing.html', context)
    if not request.user.groups.filter(name='moderators').exists():
        context = {}
        return redirect('index')

    confession_list = ConfessionRequest.objects.all()
    confession_list = confession_list.filter(approved = False).order_by("-timestamp")
    context = {'confessions':confession_list,
               
               'is_moderator':request.user.groups.filter(name='moderators').exists()}
    return render(request, 'pending.html', context)

def approve_request(request):

    data = json.loads(request.body)
    request_id = data['request_id']
    action = data['action']
    user = request.user
    
    confession_request = ConfessionRequest.objects.get(id=request_id)

    if action == 'approve' and user.groups.filter(name='moderators').exists():
        confession = Confession(content=confession_request.content, ip_address=confession_request.ip_address)
        confession.save()
        confession_request.delete()
    elif action == 'reject' and user.groups.filter(name='moderators').exists():
        confession_request.delete()
    else:
        pass

    return JsonResponse("Confession was approved", safe=False)

def report_logs(request):
    if not request.user.is_authenticated:
        context = {}
        return render(request, 'landing.html', context)
    if not request.user.groups.filter(name='moderators').exists():
        context = {}
        return redirect('index')

    report_list = ConfessionReport.objects.all()
    report_list = report_list.filter(complete=False).order_by("-timestamp")
    context = {'reports':report_list,
               'is_moderator':request.user.groups.filter(name='moderators').exists()}
    return render(request, 'reports.html', context)

def report_confession(request, id):

    if not request.user.is_authenticated:
        return redirect('index')

    confession = get_object_or_404(Confession, pk=id)
    if confession.visibility == False:
        context = {'is_moderator':request.user.groups.filter(name='moderators').exists()}
        return render(request, 'reported_already.html',context)

    form = ConfessionReportForm(request.POST or None)
    if form.is_valid() and request.user.is_authenticated:
        form.instance.user = request.user
        form.instance.confession = confession
        form.save()
        return redirect('index')

    context = {'form':form, 'is_moderator':request.user.groups.filter(name='moderators').exists()}

    return render(request, "report_confession.html", context)
    
    
def approve_report(request):

    data = json.loads(request.body)
    report_id = data['report_id']
    action = data['action']
    user = request.user

    confession = get_object_or_404(ConfessionReport, pk=report_id).confession
    #confession = get_object_or_404(Confession, pk=confession_id)

    if action == 'approve' and user.groups.filter(name='moderators').exists():
        confession.visibility = False
        confession.save()
        ConfessionReport.objects.filter(confession=confession).update(complete = True, removed=True)

    elif action == 'ignore' and user.groups.filter(name='moderators').exists():
        confession.save()
        ConfessionReport.objects.filter(confession=confession).update(complete = True)
    else:
        pass

    return JsonResponse("Report was approved", safe=False)

def about(request):
    context = {'is_moderator':request.user.groups.filter(name='moderators').exists()}
    return render(request, 'about.html', context)