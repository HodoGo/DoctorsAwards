from django.contrib import admin
from django.db import models

from awards.models import Award,Doctor,Post,Lpu,AwardType


class AwardInline(admin.TabularInline):
  model = Award
  extra = 0

class AwardTypeAdmin(admin.ModelAdmin):
  model = AwardType

class AwardAdmin(admin.ModelAdmin):
  list_display = ('number_award','type_award','date_order_award','doctor','lpu')
  def lpu(self, obj):
        return obj.doctor.lpu

class DoctorAdmin(admin.ModelAdmin):
  list_display = ('get_fio','birthday','lpu')
  inlines = [AwardInline]
  list_filter = ('lpu',)
  search_fields = ['lastname']
  list_per_page = 30

  def get_fio(self,obj):
    return obj.lastname + ' ' + obj.firstname+' '+obj.fathername
  get_fio.admin_order_field  = 'lastname'  #Allows column order sorting
  get_fio.short_description = 'ФИО'  #Renames column head

class LpuAdmin(admin.ModelAdmin):
  list_display = ('name_lpu','count_doctors')  

admin.site.register(Award,AwardAdmin)
admin.site.register(AwardType,AwardTypeAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Post)
admin.site.register(Lpu,LpuAdmin)
