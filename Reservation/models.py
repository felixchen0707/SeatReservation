from django.db import models


# Create your models here.

class UserInfo(models.Model):
    """用户信息"""

    username = models.CharField(verbose_name="用户名", max_length=32)
    mobile_phone = models.CharField(verbose_name="手机号", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    identity_choice = (
        (1, "用户"),
        (2, "管理员")
    )
    identity = models.SmallIntegerField(verbose_name="身份", choices=identity_choice, default=1)
    breaking = models.IntegerField(verbose_name="爽约次数", default=0)

    def __str__(self):
        return self.username


class Region(models.Model):
    """自习室区域"""
    name = models.CharField(verbose_name="分区名称", max_length=32)
    available_choice = (
        (1, "开放"),
        (2, "未开放")
    )
    available = models.SmallIntegerField(verbose_name="状态", choices=available_choice)

    def __str__(self):
        return self.name


class Seat(models.Model):
    """自习位置"""
    belonging = models.ForeignKey(verbose_name="所属区域", to="Region", to_field="id", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="座位名称", max_length=32)
    available_choice = (
        (1, "已预约"),
        (2, "可预约"),
        (3, "暂不开放")
    )
    available_am = models.SmallIntegerField(verbose_name="上午状态", choices=available_choice, default=2)
    available_pm = models.SmallIntegerField(verbose_name="下午状态", choices=available_choice, default=2)

    def __str__(self):
        return self.belonging.name + self.name


class ReservationHistory(models.Model):
    """预约历史"""
    seat = models.ForeignKey(verbose_name="预约座位", to="Seat", to_field="id", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="预约人", to="UserInfo", to_field="id", on_delete=models.CASCADE)
    period_choice = (
        (1, "上午"),
        (2, "下午")
    )
    period = models.SmallIntegerField(verbose_name="预约时段", choices=period_choice)
    reservation_time = models.DateTimeField(verbose_name="预约时间")
    finished_choice = (
        (1, "未签退"),
        (2, "已签退"),
        (3, "已取消")
    )
    finished = models.SmallIntegerField(verbose_name="签退状态", choices=finished_choice, default=1)

    def __str__(self):
        return self.user.username


class UnfinishedReservation(models.Model):
    """未结束的预约事务"""
    unfinished = models.ForeignKey(verbose_name="未结束的预约", to="ReservationHistory", to_field="id",
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.unfinished.user.username + "预约的" + self.unfinished.seat.belonging.name + self.unfinished.seat.name
