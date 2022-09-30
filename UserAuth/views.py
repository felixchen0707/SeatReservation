from django.shortcuts import render, HttpResponse, redirect
from io import BytesIO

from UserAuth.utils.Forms import RegisterForm, LoginForm
from UserAuth.utils.verificationCode import check_code
from Reservation import models


def register_and_login(request, nid):
    if request.method == "GET":
        if nid == 1:
            form = RegisterForm(request=request)
        else:
            form = LoginForm(request=request)
        context = {
            'form': form,
            'nid': nid
        }
        return render(request, 'UserAuth/register_and_login.html', context=context)

    if nid == 1:
        form = RegisterForm(data=request.POST, request=request)
    else:
        form = LoginForm(data=request.POST, request=request)

    if not form.is_valid():
        context = {
            'form': form,
            'nid': nid
        }
        return render(request, 'UserAuth/register_and_login.html', context=context)

    if nid == 1:
        form.instance.identity = 1
        form.instance.breaking = 0
        form.save()

    row_obj = models.UserInfo.objects.filter(username=form.cleaned_data['username']).first()
    request.session["user_info"] = {
        'id': row_obj.id,
        'username': row_obj.username
    }
    request.session.set_expiry(60 * 60 * 24 * 7)  # 7天免登录
    return redirect('/')


def generate_verification_code(request):
    stream = BytesIO()
    img, code = check_code()
    # img 储存到内存流中
    img.save(stream, 'png')
    request.session["verification_code"] = code
    request.session.set_expiry(60)  # 验证码60秒有效期
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.clear()
    return redirect('/userauth/login/1/')
