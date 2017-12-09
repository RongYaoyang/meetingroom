import json
from datetime import datetime
from django.shortcuts import render,redirect,HttpResponse
from app01 import models
# Create your views here.


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        user_obj = models.User.objects.filter(name=user,pwd=pwd).first()
        if user_obj:
            request.session['user'] = {'user':user,'is_login':True}
            print(request.session['user'])
            return redirect('/main/')
        else:
            return render(request, 'login.html')


def index(request,date=None):
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
        # print(date)
    if request.is_ajax():
        if request.method == 'GET':
            date = request.GET.get('date')
            return HttpResponse('/main/'+date)
        elif request.method == 'POST':
            data_json = request.body
            data = eval(json.loads(data_json))
            '''{"talkroom":"马尔代夫","time":"13:00","date":"2017-12-07","user":"egon"}'''
            # print(data)
            if data.get('date'):
            #是否有此用户没有添加，有就删除
                room_user = models.Date.objects.filter(date=data['date'],time=data['time'],
                                                       talkroom__title=data['talkroom'],
                                                       user__name=data['user'])

                if room_user:
                    room_user.delete()
                else:
                    talkroom = models.TalkRoom.objects.filter(title=data['talkroom']).first()
                    user = models.User.objects.filter(name=data['user']).first()
                    new_date = models.Date.objects.create(date=data['date'],time=data['time'])
                    new_date.talkroom.add(talkroom)
                    new_date.user.add(user)
                return HttpResponse('/main/')
            else:return HttpResponse('/main/')

    if request.method == 'GET':
        user_status = request.session.get('user')
        time = models.Time.objects.all()
        talkrooms = models.TalkRoom.objects.all().order_by('id')
        # print(date)
        ordered_time = models.Date.objects.filter(date=date).values('talkroom__id',"time",
                                                                         'user__name')
        return render(request,'main.html',{'time':time,'order_time':ordered_time,
                                           'talkrooms':talkrooms,'user':user_status})


def user(request, user=None):
    # print(user)
    name = request.session.get('user')
    if request.method == 'GET':
        if not user:
            # print('1')
            return HttpResponse('<h1>404 NOT FOUND</h1>')
        user_obj = models.User.objects.filter(name=user).first()
        if user_obj:
            # print('2')
            user_order = models.User.objects.filter(name=user).values('user_date__date','user_date__time','user_date__talkroom__title').order_by('user_date__date','user_date__time')
            return render(request,'user_order.html', {'user_order':user_order,'user':name})
        else:
            return HttpResponse('<h1>404 NOT FOUND</h1>')
    else:
        return HttpResponse('<h1>404 NOT FOUND</h1>')