from django.contrib import admin
from django.db import models
from easy_select2 import select2_modelform
from awards.models import Award,Doctor,Post,Lpu,AwardType
from django.urls import reverse
from rangefilter.filters import DateRangeFilter
from docxtpl import DocxTemplate
import os
from django.http import HttpResponse

class AwardInline(admin.TabularInline):
  model = Award
  extra = 0

class AwardTypeAdmin(admin.ModelAdmin):
  model = AwardType

class AwardAdmin(admin.ModelAdmin):
  form = select2_modelform(Award)
  list_display = ('incoming_num','incoming_date','doctor','type_award','lpu','number_award','date_order_award','status','refused_text')
  ordering = ('-incoming_date',)
  list_filter = (('incoming_date', DateRangeFilter),'year_award','status',)
  def lpu(self, obj):
    return obj.doctor.lpu 
  lpu.short_description = 'ЛПУ'
  lpu.admin_order_field = 'doctor__lpu__name_lpu'
  search_fields = ['incoming_num','doctor__lastname']
  list_display_links = ['incoming_num','doctor']


class DoctorAdmin(admin.ModelAdmin):
  form = select2_modelform(Doctor)
  list_display = ('get_fio','birthday','lpu','count_awards')
  inlines = [AwardInline]
  list_filter = (('award__incoming_date', DateRangeFilter),)
  search_fields = ['lastname','award__incoming_num']
  actions = ['export_to_docx']
  list_per_page = 30

  def get_fio(self,obj):
    return obj.lastname + ' ' + obj.firstname+' '+obj.fathername
  get_fio.admin_order_field  = 'lastname'  #Allows column order sorting
  get_fio.short_description = 'ФИО'  #Renames column head
  def export_to_docx(self, request, queryset): 
    _PATH = os.path.abspath(os.path.dirname(__file__))
    DOCX_TEMP = os.path.join(_PATH, 'static', 'my_word_template.docx')
    doc = DocxTemplate(DOCX_TEMP)
    context = { 'company_name' : "Отчет export_to_docx",
          'object_list': queryset
            }
    doc.render(context)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=download.docx'
    doc.save(response)           
    message_bit = "Выгружен отчет в docx"    
    self.message_user(request, "%s успешно!" % message_bit)  
    return response   


class LpuAdmin(admin.ModelAdmin):
  list_display = ('name_lpu','count_doctors')  

admin.site.register(Award,AwardAdmin)
admin.site.register(AwardType,AwardTypeAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Post)
admin.site.register(Lpu,LpuAdmin)
