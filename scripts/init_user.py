"""
离线脚本：
运行离线脚本，自动创建初始化数据
"""
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)  # 添加项目路径只系统环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SeatReservation.settings")
django.setup()  # os.environ['DJANGO_SETTINGS_MODULE']

from Seat_Management import models

# 创建用户数据

user_data_dict1 = {
    "username": "Felix",
    "password": "123",
    "mobile_phone": "1383838338",
    "identity": 2,
    "breaking": 0
}

user_data_dict2 = {
    "username": "Alex",
    "password": "456",
    "mobile_phone": "1383838338",
    "identity": 1,
    "breaking": 2
}

user_data_dict_list = [user_data_dict1, user_data_dict2]

for user_data_dict in user_data_dict_list:
    if not models.UserInfo.objects.filter(**user_data_dict).exists():
        models.UserInfo.objects.create(**user_data_dict)

# 创建区域数据

region_data_dict1 = {
    "name": "A",
    "available": 1
}
region_data_dict2 = {
    "name": "B",
    "available": 1
}

region_data_dict_list = [region_data_dict1, region_data_dict2]

for region_data_dict in region_data_dict_list:
    if not models.Region.objects.filter(**region_data_dict).exists():
        models.Region.objects.create(**region_data_dict)


