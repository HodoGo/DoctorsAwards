from django.db import models
from django.urls import reverse

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
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
      return self.lastname +' ' + self.firstname
  def get_absolute_url(self):
    return reverse('doctor-detail', kwargs={'pk': self.pk})    

  class Meta:
    verbose_name = 'Врач'
    verbose_name_plural = 'Врачи'     

class Award(models.Model):
  name_award = models.CharField(max_length=50)
  number_award = models.IntegerField()
  date_order_award = models.DateField()
  doctor = models.ForeignKey('Doctor', on_delete=models.PROTECT)

  def __str__(self):
    return self.name_award + ' №' + str(self.number_award) + ' от ' + self.date_order_award.strftime("%d.%m.%Y")

  class Meta:
    verbose_name = 'Награда'
    verbose_name_plural = 'Награды'     
