import json
import datetime

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Reservation import models


# Create your views here.
def index(request):
    return render(request, 'base.html')


def seatsList(request):
    query_set = models.Seat.objects.all()

    # 返回前端
    context = {
        'query_set': query_set
    }
    return render(request, 'Reservation/seats_list.html', context)


@csrf_exempt
def reserve_seat(request):
    # 验证POST请求
    if not request.method == "POST":
        data_dict = {
            'status': False,
            'message': "非法访问"
        }
        return HttpResponse(json.dumps(data_dict))

    target_seat = models.Seat.objects.filter(id=request.POST.get('reserve_id')).first()
    target_period = int(request.POST.get('period'))
    # 验证座位是否空余
    print(target_period)
    print(type(target_period))
    print(target_seat.available_am)
    boolean = (target_period == 1 and (not target_seat.available_am == 2)) or (
            target_period == 2 and (not target_seat.available_pm == 2))
    print(boolean)
    if boolean:
        data_dict = {
            'status': False,
            'message': "无法预约的座位"
        }
        return HttpResponse(json.dumps(data_dict))

    # 读取用户信息
    target_user = models.UserInfo.objects.filter(id=request.session["user_info"]['id']).first()
    data_save = {
        'seat': target_seat,
        'user': target_user,
        'period': target_period,
        'finished': 1,
        'reservation_time': datetime.datetime.now()
    }
    models.ReservationHistory.objects.create(**data_save)  # 将预约数据存入数据库

    models.UnfinishedReservation.objects.create(
        unfinished=models.ReservationHistory.objects.filter(**data_save).first()
    )  # 将未完成数据写入数据库

    # 更改座位状态
    if target_period == 1:
        target_seat.available_am = 1
        target_seat.save()
    if target_period == 2:
        target_seat.available_pm = 1
        target_seat.save()

    # 返回状态信息
    data_dict = {
        'status': True,
        'message': "预约成功！"
    }
    return HttpResponse(json.dumps(data_dict))
