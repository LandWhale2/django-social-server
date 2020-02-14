from django.contrib import admin
from . import models
# Register your models here.



@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'active', 'gender', 'email', 'nickname', 'updated_ay', 'age', 'rating','image1']

    actions = ['make_active','make_inactive']

    def make_active(self, request, queryset):
        updated_count = queryset.update(active = True) #queryset.update
        self.message_user(request, '{}건의 포스팅을 active 상태로 변경'.format(updated_count)) #django message framework 활용
    make_active.short_description = '지정 포스팅을 active 상태로 변경'

    def make_inactive(self, request, queryset):
        updated_count = queryset.update(active = False) #queryset.update
        self.message_user(request, '{}건의 포스팅을 inactive 상태로 변경'.format(updated_count)) #django message framework 활용
    make_inactive.short_description = '지정 포스팅을 inactive 상태로 변경'
