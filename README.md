## 设置步骤

### 建立数据库

首先请创建数据库，并在`settings.py`中的`DATABASES`中输入相关的信息。而后执行

```
python manage.py makemigrations
python manage.py migrate
```

创建数据库的表。

### 创建管理员

本项目使用了Django自带的管理后台，第一次使用你需要创建超级管理员。

```
python manage.py createsuperuser
```

而后登录`/admin/`即可。