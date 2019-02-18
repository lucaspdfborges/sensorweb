from django.db import models
from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser, User
from django.utils import timezone
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth import get_user_model as user_model
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from django.dispatch import receiver
#from django.contrib.gis.db import models

class Linhas(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='media', blank=True)

    def __str__(self):
        return self.nome

class Achievement(models.Model):
    FIELDS = (
             ('A', 'Formação Acadêmica'),
             ('B', 'Formação Complementar'),
             ('C', 'Publicação'),
             ('D', 'Produtos, Inovações e Aplicações')
            )

    pesquisador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campo = models.CharField(max_length=1, choices=FIELDS)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    texto = models.TextField()
    link = models.URLField(blank=True);

    def __str__(self):
        return self.pesquisador

    def getObject():
        return self

class Experimento(models.Model):
    pesquisador = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pesquisador' , on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    last_seen = models.DateTimeField(default=timezone.now)
    last_data = models.FloatField(default=0)
    created = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    #location = models.PointField()
    #group = models. ...

    def __str__(self):
        return self.name

class DashData(models.Model):
    experimento = models.ForeignKey(Experimento, related_name='experimento', on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    dado = models.FloatField()

    def __str__(self):
        return self.experimento.name


class Paper(models.Model):
    pesquisador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_publicacao = models.DateField()
    titulo = models.TextField()
    revista = models.TextField()
    campos = models.ManyToManyField(Linhas)
    link = models.URLField(blank=True);

    def __str__(self):
        return self.titulo

class CustomUser(AbstractUser):

    def __str__(self):
        return self.email

class Profile(models.Model):

    GRAD_CHOICES = (
             ('B', 'Bacharel'),
             ('M', 'Mestre'),
             ('D', 'Doutor(a)')
            )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, blank=True)
    graduacao = models.CharField(max_length=200, blank=True)
    titulo = models.CharField(max_length=1, choices=GRAD_CHOICES, blank=True)
    email = models.EmailField(blank=True)
    foto = models.ImageField(upload_to='media', default='/media/avatar.png', blank=True)
    pesquisas = models.ManyToManyField(Linhas)

    def __str__(self):
        return self.nome

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
