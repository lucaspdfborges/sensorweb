from django import forms
from django.forms import formset_factory
from django.contrib.admin import widgets
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import  Profile, Linhas, CustomUser, Achievement, Paper, DashData, Experimento

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

class AchievementForm(forms.ModelForm):

    data_inicio = forms.DateField(widget=forms.SelectDateWidget(years=range(1970,2025)))
    data_fim = forms.DateField(widget=forms.SelectDateWidget(years=range(1970,2025)))

    class Meta:
        model = Achievement
        fields = ( 'data_inicio', 'data_fim', 'texto', 'link')

class ProfileForm(forms.ModelForm):

    GRAD_CHOICES = (
             ('B', 'Bacharel'),
             ('M', 'Mestre'),
             ('D', 'Doutor(a)')
            )

    pesquisas = forms.ModelMultipleChoiceField(
        widget = forms.CheckboxSelectMultiple,
        queryset=Linhas.objects.all())

    titulo = forms.ChoiceField(
        widget = forms.RadioSelect(),
        choices=GRAD_CHOICES)

    class Meta:
        model = Profile
        fields = ('nome','graduacao','titulo','email','foto', 'pesquisas')

class PaperForm(forms.ModelForm):

    campos = forms.ModelMultipleChoiceField(
        widget = forms.CheckboxSelectMultiple,
        queryset=Linhas.objects.all())

    data_publicacao = forms.DateField(widget=forms.SelectDateWidget(years=range(1970,2025)))

    class Meta:
        model = Paper
        fields = ('data_publicacao','titulo','revista','link','campos')

class ExperimentoForm(forms.ModelForm):

    class Meta:
        model = Experimento
        fields = ('name','description')

class DashDataForm(forms.ModelForm):

    data = forms.DateTimeField(widget=forms.SelectDateWidget())

    class Meta:
        model = DashData
        fields = ('data','dado')

DashDataset = formset_factory(DashDataForm, extra=1)

class LinhaForm(forms.ModelForm):

    class Meta:
        model = Linhas
        fields = ('nome','descricao','imagem')
