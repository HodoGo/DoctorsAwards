from django.db import models
from django.urls import reverse
from django.forms import ModelForm

class Lpu(models.Model):
  code_lpu = models.IntegerField(verbose_name='Код лпу')
  name_lpu = models.CharField(max_length=200,verbose_name='Наименование')

  def __str__(self):
    return self.name_lpu
  
  class Meta:
    verbose_name = 'ЛПУ'
    verbose_name_plural = 'ЛПУ'
        
  @property  
  def count_doctors(self):
    return self.doctors.count()
  

class Post(models.Model):
  name_post = models.CharField(max_length=150,verbose_name='Наименование')

  def __str__(self):
        return self.name_post

  class Meta:
    verbose_name = 'Должность'
    verbose_name_plural = 'Должности'     

class Doctor(models.Model):
  lastname = models.CharField(max_length=100,verbose_name='Фамилия')
  firstname = models.CharField(max_length=100,verbose_name='Имя')
  fathername = models.CharField(max_length=100,verbose_name='Отчество')
  birthday = models.DateField(verbose_name='Дата рождения')
  lpu = models.ForeignKey('Lpu', on_delete=models.PROTECT,related_name='doctors',verbose_name='ЛПУ')
  post = models.ForeignKey('Post', on_delete=models.PROTECT,verbose_name='Должность')
  experience_all = models.IntegerField(verbose_name='общий')
  experience_branch = models.IntegerField(verbose_name='в отрасли')
  experience_last = models.IntegerField(verbose_name='на последнем месте')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
      return '%s %s %s %s' % (self.lastname, self.firstname,self.fathername,self.birthday.strftime("%m.%d.%Y")) 
  def get_absolute_url(self):
    return reverse('doctor-detail', kwargs={'pk': self.pk})
  @property  
  def count_awards(self):
    return self.award.count()    

  class Meta:
    verbose_name = 'Сотрудник'
    verbose_name_plural = 'Сотрудники'     

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ['lastname', 'birthday']

class Award(models.Model):
  AWARD_STATUS = (
      ('draft','На расмотрении'),
      ('refused','Отклонен'),
      ('approved','Подтвержден')
    )

  incoming_num = models.IntegerField(verbose_name='Вх. №')
  incoming_date = models.DateField(verbose_name='Вх. дата')
  doctor = models.ForeignKey('Doctor', on_delete=models.PROTECT,related_name='award',verbose_name='Сотрудник')
  type_award = models.ForeignKey('AwardType',on_delete=models.PROTECT,verbose_name='Тип награды')
  year_award = models.IntegerField(verbose_name='Год награды')
  number_award = models.CharField(max_length=50,verbose_name='Номер приказа',null=True,blank=True)
  date_order_award = models.DateField(verbose_name='Дата приказа',null=True,blank=True)  
  status = models.CharField(max_length=10,choices=AWARD_STATUS)
  refused_text = models.CharField(max_length=200,verbose_name="Причина отказа",null=True,blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.type_award) + ' №' + str(self.incoming_num) + ' от ' + self.incoming_date.strftime("%d.%m.%Y")

 

  class Meta:
    verbose_name = 'Награда'
    verbose_name_plural = 'Награды'    
    ordering = ['-incoming_date']

class AwardType(models.Model):
  awardtype_name = models.CharField(max_length=50)

  def __str__(self):
      return self.awardtype_name

  class Meta:
    verbose_name = 'Вид наград'
    verbose_name_plural = 'Виды нарад'  
