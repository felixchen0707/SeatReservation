import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Reservation import models


# Create your views here.
def my_reservation(request):
    target_user = models.UserInfo.objects.filter(id=request.session['user_info']['id']).first()
    unfinished_query_set = models.ReservationHistory.objects.filter(user=target_user, finished=1).order_by(
        '-reservation_time')
    finished_query_set = models.ReservationHistory.objects.filter(user=target_user, finished__in=[2, 3]).order_by(
        '-reservation_time')

    context = {
        'unfinished': unfinished_query_set,
        'finished': finished_query_set
    }
    return render(request, 'My/My_Reservation.html', context=context)


@csrf_exempt
def cancel_reservation(request):
    if not request.method == "POST":
        return HttpResponse("非法访问")

    target_id = int(request.POST.get('cancelId'))
    target_history = models.ReservationHistory.objects.filter(id=target_id).first()

    # 更新状态
    target_history.finished = 3
    target_history.save()

    # 从未结束列表中删除
    models.UnfinishedReservation.objects.filter(unfinished=target_history).delete()

    # 释放座位
    target_seat = target_history.seat
    target_period = target_history.period
    if target_period == 1:
        target_seat.available_am = 2
    if target_period == 2:
        target_seat.available_pm = 2
    target_seat.save()

    data_dict = {
        'status': True,
        'message': "取消成功"
    }

    return HttpResponse(json.dumps(data_dict))
