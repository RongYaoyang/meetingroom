from django.contrib import admin
from app01 import models
# Register your models here.


admin.site.register(models.User)
admin.site.register(models.TalkRoom)
admin.site.register(models.Date)
admin.site.register(models.Time)