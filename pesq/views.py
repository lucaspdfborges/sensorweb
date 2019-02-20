from django.shortcuts import render, get_object_or_404
from .models import Linhas, Profile, CustomUser, Achievement, Paper, DashData, Experimento
from .forms import  LinhaForm, CustomUserCreationForm, CustomUserChangeForm, ProfileForm, AchievementForm, PaperForm, DashDataForm, DashDataset, ExperimentoForm
from .serializers import DashDataSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import TemplateView
from rest_framework import generics
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from django.http import JsonResponse
from django.db.models import Q
import csv
import math
import datetime
from operator import attrgetter
from django.utils import timezone

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your views here.
def home(request):
    return render(request, 'pesq/home.html')

def linhas(request):
    linhasPesquisa = Linhas.objects.all()
    return render(request, 'pesq/linhas.html', {'linhasPesquisa':linhasPesquisa})

def pesq_list(request):
    pesquisadores = Profile.objects.all()
    linhasPesquisa = Linhas.objects.all()
    return render(request, 'pesq/pesq_list.html', {'pesquisadores':pesquisadores, 'linhasPesquisa':linhasPesquisa})

def pesq_detail(request, pk):
    user = CustomUser.objects.get(pk=pk)
    usuario = Profile.objects.get(pk=pk)
    curriculum = Achievement.objects.filter(pesquisador=pk)
    cvAcademica = Achievement.objects.filter(pesquisador=pk, campo='A')
    cvComplementar = Achievement.objects.filter(pesquisador=pk, campo='B')
    cvPublicacao = Achievement.objects.filter(pesquisador=pk, campo='C')
    cvInovacao = Achievement.objects.filter(pesquisador=pk, campo='D')
    cvPaper = Paper.objects.filter(pesquisador=pk)
    fields = usuario.pesquisas.all()
    return render(request, 'pesq/pesq_detail.html', {'usuario': usuario, 'fields': fields, 'curriculum':curriculum, 'cvAcademica' : cvAcademica, 'cvComplementar' : cvComplementar, 'cvPublicacao' : cvPublicacao, 'cvInovacao': cvInovacao, 'cvPaper': cvPaper})

def pesq_detail_add(request):
    usuario = request.user.profile
    pk = usuario.pk
    curriculum = Achievement.objects.filter(pesquisador=pk)
    cvAcademica = Achievement.objects.filter(pesquisador=pk, campo='A')
    cvComplementar = Achievement.objects.filter(pesquisador=pk, campo='B')
    cvPublicacao = Achievement.objects.filter(pesquisador=pk, campo='C')
    cvInovacao = Achievement.objects.filter(pesquisador=pk, campo='D')
    cvPaper = Paper.objects.filter(pesquisador=pk)
    fields = usuario.pesquisas.all()
    return render(request, 'pesq/pesq_detail_add.html', {'usuario': usuario, 'fields': fields, 'curriculum':curriculum, 'cvAcademica' : cvAcademica, 'cvComplementar' : cvComplementar, 'cvPublicacao' : cvPublicacao, 'cvInovacao': cvInovacao, 'cvPaper': cvPaper})

def linha_detail(request, pk):
    linha = Linhas.objects.get(pk=pk)
    return render(request, 'pesq/linha_detail.html', {'linha':linha})

def usuario_cadastrar(request):
    if request.method == 'POST':
        userForm = CustomUserCreationForm(request.POST)
        if userForm.is_valid():
            user = userForm.save()
            user = authenticate(username=userForm.cleaned_data['username'],
                                    password=userForm.cleaned_data['password1'],
                                    )
            login(request, user)
            return redirect('update_profile')
    else:
        userForm = CustomUserCreationForm()
    return render(request, 'pesq/signup.html', {'userForm': userForm})

def reset_pwd(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Profile.objects.filter(user__email = 'lucaspdfborges@gmail.com').exists():
            sendMail(email)
            messages.success(request, 'E-mail enviado com sucesso! \n Verifique sua caixa de entrada do email')
            return render(request, 'registration/login.html')
        else:
            messages.warning(request, 'Erro : e-mail não cadastrado.')
            return render(request, 'pesq/reset_pwd.html')
    return render(request, 'pesq/reset_pwd.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('home')
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    usuario = request.user.profile
    pk = usuario.pk
    return render(request, 'pesq/profile.html', {
        'profile_form': profile_form, 'usuario': usuario
    })

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@login_required
def dashboard_options(request):
    return render(request, 'dash/dashboard_options.html')

class DashDataInsert(generics.CreateAPIView):
    '''
    POST
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DashDataSerializer

    def post(self, request,*args, **kwargs):
        experimento = request.data.get("experimento", "")
        dado = request.data.get("dado","")

        Exp = Experimento.objects.filter(pesquisador=request.user, name=experimento).first()

        post = DashData()
        post.experimento = Exp
        post.dado = dado
        post.save()

        Exp.last_seen = timezone.now()
        Exp.last_data = dado
        Exp.save()

        responseData = {
            'datetime':post.data,
            'experimento':experimento,
            'dado':dado
        }
        return JsonResponse(responseData)

class DashDataView(generics.ListAPIView):
    '''
    Provides a get method handler
    '''
    queryset = DashData.objects.all()
    serializer_class = DashDataSerializer
    permission_classes = (permissions.IsAuthenticated,)

@login_required
def insert_achievement(request, campo):
    if request.method == 'POST':
        achievement_form = AchievementForm(request.POST)
        if achievement_form.is_valid():
            post = achievement_form.save(commit=False)
            post.pesquisador = request.user
            post.campo = campo
            post.save()
            return HttpResponse('<script type="text/javascript">window.opener.parent.location.href = "/curriculum/";window.close();</script>')
    else:
        achievement_form = AchievementForm()
    return render(request, 'pesq/achievement.html', {'achievement_form': achievement_form})

@login_required
def insert_paper(request):
    if request.method == 'POST':
        paper_form = PaperForm(request.POST)
        if paper_form.is_valid():
            paper = paper_form.save(commit=False)
            paper.pesquisador = request.user
            paper.save()
            return HttpResponse('<script type="text/javascript">window.opener.parent.location.href = "/curriculum/";window.close();</script>')
    else:
        paper_form = PaperForm()
    return render(request, 'forms/paper.html', {'paper_form': paper_form})

@login_required
def delete_achievement(request, pk):
    post = Achievement.objects.filter(pk=pk)
    post.delete()
    return redirect('pesq_detail_add')

@login_required
def delete_paper(request, pk):
    paper = Paper.objects.filter(pk=pk)
    paper.delete()
    return redirect('pesq_detail_add')

@login_required
def linha_cadastrar(request):
    if request.method == 'POST':
        form = LinhaForm(request.POST)
        if form.is_valid():
            linha = form.save(commit=True)
            return redirect('home')
    else:
        form = LinhaForm()
    linhaForm = LinhaForm()
    return render(request, 'pesq/linha_cadastro.html', {'linhaForm': linhaForm})


@login_required
def dashboard_exps(request):
    usuario = request.user.profile
    pk = usuario.pk
    exps = DashData.objects.values('experimento').distinct().filter(pesquisador=pk)

    return render(request, 'dash/dashboard_exps.html', {'exps':exps} )

@login_required
def dashboard_chart(request):
    usuario = request.user.profile
    pk = usuario.pk
    datagroup = DashData.objects.values('experimento').distinct().filter(pesquisador=pk)
    lastData = DashData.objects.values('dado').filter(pesquisador=pk).last()

    return render(request, 'dash/dashboard_chart.html', {'datagroup':datagroup, 'lastData':lastData} )

@login_required
def dashboard_real_time(request):
    usuario = request.user.profile
    pk = usuario.pk
    experimentos = Experimento.objects.filter(pesquisador=pk)

    return render(request, 'dash/dashboard_real_time.html', {'experimentos':experimentos} )

@login_required
def sensor_delete(request):
    if request.method == 'POST':
        expID = request.POST['expID']
        usuario = request.user.profile
        pk = usuario.pk
        experimento = Experimento.objects.filter(pesquisador=pk,pk__in=expID)
        experimento.delete()
        return HttpResponse('sensor deleted')

@login_required
def sensor_update(request):
    if request.method == 'POST':

        expID = request.POST['expID']
        expName = request.POST['expName']
        expDescription = request.POST['expDescription']

        usuario = request.user.profile
        pk = usuario.pk
        experimento = Experimento.objects.filter(pesquisador=pk,pk__in=expID).first()

        experimento.name = expName
        experimento.description = expDescription
        experimento.save()

        return HttpResponse('sensor updated')

@login_required
def dashboard_chart_detail(request):

    usuario = request.user.profile
    pk = usuario.pk

    experimentos = Experimento.objects.filter(pesquisador=pk)
    dataExp = DashData.objects.filter(experimento__in=experimentos)

    maxValue = dataExp.order_by('dado').reverse().first().dado
    minValue =  dataExp.order_by('dado').first().dado

    oldestDateTime = dataExp.order_by('data').first().data
    oldestDate = str(oldestDateTime)[0:10]
    oldestTime = str(oldestDateTime)[11:19]

    nowDateTime = str(datetime.datetime.now())
    nowDate = nowDateTime[0:10]
    nowTime = nowDateTime[11:19]

    return render(request, 'dash/dashboard_detail.html', {'dataExp':dataExp, 'experimentos':experimentos, 'maxValue': maxValue, 'minValue':minValue, 'oldestDate': oldestDate, 'oldestTime': oldestTime, 'nowDate': nowDate, 'nowTime': nowTime} )

@login_required
def dashboard_update_data(request):
    if request.method == 'POST':

        id = request.POST['idValue']
        dado = request.POST['dadoValue']
        date = request.POST['datetimeValue']

        dashdata = DashData.objects.get(pk=id)
        dashdata.dado = dado
        dashdata.data = date
        dashdata.save()

        return HttpResponse('200')

@login_required
def dashboard_insert_data(request):

    usuario = request.user.profile
    pk = usuario.pk

    if request.method == 'POST':

        expList = request.POST.getlist('expList[]')
        dateList = request.POST.getlist('dateList[]')
        timeList = request.POST.getlist('timeList[]')
        valueList = request.POST.getlist('valueList[]')

        for i in range(len(expList)):
            Exp = Experimento.objects.filter(pesquisador=pk, name=expList[i]).first()
            dashdata = DashData()
            dashdata.experimento = Exp
            dashdata.data = dateList[0]+" "+ timeList[0]
            dashdata.dado = float(valueList[0])
            dashdata.save()

    return render(request, 'dash/dashboard_real_time.html')


@login_required
def dashboard_insert_data_page(request):
    usuario = request.user.profile
    pk = usuario.pk
    experimentos = Experimento.objects.filter(pesquisador=pk)
    return render(request, 'dash/dashboard_type_data.html', { 'experimentos':experimentos} )


class DashDataManualInsert(TemplateView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        experimento = request.POST['experimento']

        yearList = request.POST.getlist('yearList[]')
        monthList = request.POST.getlist('monthList[]')
        dayList = request.POST.getlist('dayList[]')

        hourList = request.POST.getlist('hourList[]')
        minuteList = request.POST.getlist('minuteList[]')
        secondList = request.POST.getlist('secondList[]')

        valueList = request.POST.getlist('valueList[]')

        for i in range(1,len(valueList),1):
            datetime = '%s-%s-%s 0%s:0%s:0%s' % (yearList[i], monthList[i], dayList[i], hourList[i], minuteList[i], secondList[i])
            post = DashData()
            post.pesquisador = request.user
            post.data = datetime
            post.experimento = experimento
            post.dado = valueList[i]
            post.save()

        return render(request, 'dash/dashboard_type_data.html', {'experimento':experimento})

class DashDataDelete(TemplateView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        experimento = request.POST['experimento']
        idList = request.POST.getlist('idList[]')
        print(idList)

        print(DashData.objects.filter(pk__in=idList))

        DashData.objects.filter(pk__in=idList).delete()

        usuario = request.user.profile
        pk = usuario.pk
        dataExp = DashData.objects.filter(pesquisador=pk, experimento=experimento)
        return render(request, 'dash/dashboard_data.html', {'dataExp':dataExp, 'experimento':experimento} )

class DashDataSearch(TemplateView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        expNames = request.GET.getlist('expNames[]')

        initialDate = request.GET['initialDate']
        finalDate = request.GET['finalDate']

        maxValue = request.GET['maxValue']
        minValue = request.GET['minValue']

        section = int(request.GET['section'])

        lowerLim = (section - 1)*50
        upperLim = section * 50

        usuario = request.user.profile
        pk = usuario.pk

        dashList = DashData.objects.none()

        for expname in expNames:
            exp = Experimento.objects.filter(pesquisador=pk, name=expname).first()
            newDashList = DashData.objects.filter(experimento=exp)
            dashList = dashList | newDashList

        dashList = dashList.order_by('data').reverse()

        if not initialDate=='indefinido':
            dashList = dashList.filter(data__gte=initialDate)
        if not finalDate=='indefinido':
            dashList = dashList.filter(data__lte=finalDate)
        if not minValue=='indefinido':
            dashList = dashList.filter(dado__gte=minValue)
        if not maxValue=='indefinido':
            dashList = dashList.filter(dado__lte=maxValue)


        sections = math.ceil(dashList.count()/50)
        dashList = dashList[lowerLim:upperLim]

        searchData = {
            'minValue' : minValue,
            'maxValue' : maxValue,
            'initialDate' : initialDate,
            'finalDate' : finalDate,
        }

        dateList = []
        valueList = []
        sensorList = []
        pkList = []

        for dash in dashList:
            dateList.append(dash.data)
            valueList.append(dash.dado)
            sensorList.append(dash.experimento.name)
            pkList.append(dash.pk)

        searchData['dateList'] = dateList
        searchData['valueList'] = valueList
        searchData['sensorList'] = sensorList
        searchData['pkList'] = pkList
        searchData['sections'] = sections

        return JsonResponse(searchData)

@login_required
def dashdata_download(request):
    if request.method == 'GET':

        experimento = request.GET['experimento']

        initialDate = request.GET['initialDate']
        finalDate = request.GET['finalDate']

        minValue = request.GET['minValue']
        maxValue = request.GET['maxValue']

        valueList = request.GET.getlist('valueList[]')
        strValueList = str(valueList)[2:len(str(valueList))-2].split(",")

        dateList = request.GET.getlist('dateList[]')
        strDateList = str(dateList)[2:len(str(dateList))-2].split(",")

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="myfile.csv"'

        writer = csv.writer(response)
        writer.writerow(['Experimento', 'Data Inicial', 'Data Final ', 'Minimo', 'Maximo'])
        writer.writerow([experimento, initialDate, finalDate, minValue, maxValue])
        writer.writerow([' ', ' '])
        writer.writerow(['Data e hora', 'Valor'])
        for i in range(len(strValueList)):
            writer.writerow([strDateList[i], strValueList[i]])

        return response

@login_required
def dashboard_chart_data(request):
    # section one is from 0 to 49, section 2 from 50 to 99, and go on...
    lowerLim = 0
    upperLim =50
    usuario = request.user.profile
    pk = usuario.pk

    experimentos = Experimento.objects.filter(pesquisador=pk)
    dataExp = DashData.objects.filter(experimento__in=experimentos)

    maxValue = dataExp.order_by('dado').reverse().first().dado
    minValue =  dataExp.order_by('dado').first().dado

    oldestDateTime = dataExp.order_by('data').first().data
    oldestDate = str(oldestDateTime)[0:10]
    oldestTime = str(oldestDateTime)[11:19]

    nowDateTime = str(datetime.datetime.now())
    nowDate = nowDateTime[0:10]
    nowTime = nowDateTime[11:19]

    sections =  math.ceil(dataExp.count()/50)
    dataExp = dataExp[lowerLim:upperLim]

    return render(request, 'dash/dashboard_data.html', {'dataExp':dataExp, 'experimentos':experimentos, 'sections': sections, 'maxValue': maxValue, 'minValue':minValue, 'oldestDate': oldestDate, 'oldestTime': oldestTime, 'nowDate': nowDate, 'nowTime': nowTime} )

@login_required
def chart_data(request):
    if request.method == 'GET':

        usuario = request.user.profile
        pk = usuario.pk

        experimentos = request.GET.getlist('expNames[]')

        initialDate = request.GET['initialDate']
        finalDate = request.GET['finalDate']

        maxValue = request.GET['maxValue']
        minValue = request.GET['minValue']

        listXY = []

        for exp in experimentos:

            Exp = Experimento.objects.filter(pesquisador=pk, name=exp).first()

            dataset = DashData.objects.filter(experimento=Exp)

            if not initialDate=='indefinido':
                dataset = dataset.filter(data__gte=initialDate)
            if not finalDate=='indefinido':
                dataset = dataset.filter(data__lte=finalDate)
            if not minValue=='indefinido':
                dataset = dataset.filter(dado__gte=minValue)
            if not maxValue=='indefinido':
                dataset = dataset.filter(dado__lte=maxValue)

            listExpXY = []

            for i in range(len(dataset)):
                valueX = dataset[i].data.strftime('%H:%M:%S')
                valueY = dataset[i].dado
                listExpXY.append([valueX,valueY])

            listXY.append({
                'name': 'experimentos',
                'data': listExpXY,
                'marker': {
                        'enabled': False,
                    },
                'shadow': True,
                'lineWidth': 2,
                'animation': False,
                })


        chart = {
            'colors': ['#55acee', '#2f5f85', '#aac'],
            'chart': {'type': 'areaspline'},
            'title': {'text': ''},
            'yAxis': {
                        'title': {
                            'text': ''
                        }
            },
            'plotOptions':{
                'areaspline': {
                    'fillOpacity': 0.3,
                },
            },
            'legend': {
                        'enabled': False
            },
            'time':{
                'useUTC': False,
            },
            'series': listXY,
        }

        return JsonResponse(chart)



@login_required
def dashboard_all_data(request):
    if request.method == 'GET':

        usuario = request.user.profile
        pk = usuario.pk
        experimentos = Experimento.objects.filter(pesquisador=pk)

        listXY = []

        for exp in experimentos:
            dataset = DashData.objects.filter(experimento=exp)

            listExpXY = []

            for i in range(len(dataset)):
                valueX = dataset[i].data.strftime('%H:%M:%S %d/%m/%Y')
                valueY = dataset[i].dado
                listExpXY.append([valueX,valueY])

            listXY.append({
                'name': str(exp.name),
                'data': listExpXY,
                'marker': {
                        'enabled': False,
                    },
                'shadow': True,
                'lineWidth': 2,
                'animation': False,
                })


        chart = {
            'colors': ['#55acee', '#2f5f85', '#aac'],
            'chart': {'type': 'areaspline'},
            'title': {'text': ''},
            'yAxis': {
                        'title': {
                            'text': ''
                        }
            },
            'plotOptions':{
                'areaspline': {
                    'fillOpacity': 0.3,
                },
            },
            'legend': {
                        'enabled': False
            },
            'time':{
                'useUTC': False,
            },
            'series': listXY,
        }

        return JsonResponse(chart)


@login_required
def dashboard_stats(request):
    if request.method == 'GET':

        usuario = request.user.profile
        pk = usuario.pk
        experimentos = Experimento.objects.filter(pesquisador=pk)

        latest = DashData.objects.latest('data')
        total = DashData.objects.count()

        biggestDB = ''
        sizeDB = 0
        newest = Experimento.objects.latest('created').name
        latestList = []

        for exp in experimentos:
            datasetSize = DashData.objects.filter(experimento=exp).count()
            if datasetSize > sizeDB:
                biggestDB = exp.name

            latestList.append(DashData.objects.filter(experimento=exp).latest('data'))


        inactive = min(latestList, key=attrgetter('data'))

        stats = {
            'latest-name': str(latest.experimento.name),
            'latest-value': str(round(latest.dado,3)),
            'latest-datetime': latest.data.strftime('%H:%M:%S %d/%m/%Y'),
            'total-amount': str(total),
            'biggest-db': str(biggestDB),
            'newest': str(newest),
            'inactive-name':str(inactive.experimento.name),
            'inactive-datetime':str(inactive.data.strftime('%H:%M:%S %d/%m/%Y')),
            'inactive-value':str(round(inactive.dado,3)),
        }

        return JsonResponse(stats)


@login_required
def dashboard_data_amount(request):
    if request.method == 'GET':

        usuario = request.user.profile
        pk = usuario.pk

        experimento = request.GET.getlist('experimento[]')

        listXY = []

        colors= ['#55acee', '#2f5f85', '#aac', '#cac']
        colorsIter = iter(colors)

        for exp in experimento:
            Exp = Experimento.objects.filter(pesquisador=pk, name=exp).first()
            dataset = DashData.objects.filter(experimento=Exp)
            listXY.append({'name':str(exp),'y':len(dataset),'color':next(colorsIter)})
            print(exp)

        data= {
                  'chart': {
                    'plotBackgroundColor': None,
                    'plotBorderWidth': None,
                    'plotShadow': False,
                    'type': 'pie'
                  },
                  'title':None,
                  'tooltip': {
                    'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'
                  },
                  'plotOptions': {
                    'pie': {
                      'cursor': 'pointer',
                      'dataLabels': {
                        'distance': -50,
                        'enabled': True,
                        'style':{
                        }
                       }
                    }
                  },
                  'series': [{
                    'innerSize': '40%',
                    'name': 'Porcentagem',
                    'data': listXY
                  }]
                }



        return JsonResponse(data)

@login_required
def insert_sensor(request):
    if request.method == 'POST':
        experimento_form = ExperimentoForm(request.POST)
        if experimento_form.is_valid():
            post = experimento_form.save(commit=False)
            post.pesquisador = request.user
            post.save()
            return HttpResponse('<script type="text/javascript">window.opener.parent.location.href = "/dashboard/chart_real_time/";window.close();</script>')
    else:
        experimento_form = ExperimentoForm()
    return render(request, 'forms/experimento.html', {'experimento_form': experimento_form})
