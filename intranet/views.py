from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import TiInforma, Quadro, Admitido, Promocao
from datetime import date
from dotenv import load_dotenv
import requests, os

load_dotenv()

# CLIMA
API_KEY = str(os.getenv('API_KEY'))

CIDADES = [
    {'nome': 'Rio de Janeiro', 'uf': 'RJ', 'codigo': 'Rio de Janeiro,BR'},
    {'nome': 'São Paulo', 'uf': 'SP', 'codigo': 'São Paulo,BR'},
    {'nome': 'Lauro de Freitas', 'uf': 'BA', 'codigo': 'Lauro de Freitas,BR'},
]


def login_view(request):
    error_message = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # cria a sessão
            return redirect("admin_dashboard")  # redireciona para dashboard
        else:
            error_message = "Usuário ou senha inválidos."

    return render(request, "login.html", {"error_message": error_message})


@login_required
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def obter_clima(cidade_codigo, cidade_uf):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={cidade_codigo}&units=metric&lang=pt_br&appid={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        clima = {
            'cidade': f"{data['name']} - {cidade_uf}",
            'temperatura': round(data['main']['temp']),
            'descricao': data['weather'][0]['description'].capitalize(),
            'icon_code': data['weather'][0]['icon']
        }
        # Traduzir código do OpenWeatherMap para ícone do Bootstrap Icons
        icon_map = {
            '01d': 'bi-sun-fill', '01n': 'bi-moon-fill',
            '02d': 'bi-cloud-sun-fill', '02n': 'bi-cloud-moon-fill',
            '03d': 'bi-cloud-fill', '03n': 'bi-cloud-fill',
            '09d': 'bi-cloud-drizzle-fill', '09n': 'bi-cloud-drizzle-fill',
            '10d': 'bi-cloud-rain-fill', '10n': 'bi-cloud-rain-fill',
            '11d': 'bi-cloud-lightning-fill', '11n': 'bi-cloud-lightning-fill',
            '13d': 'bi-snow3', '13n': 'bi-snow3',
            '50d': 'bi-cloud-fog-fill', '50n': 'bi-cloud-fog-fill'
        }
        clima['icon_class'] = icon_map.get(clima['icon_code'], 'bi-cloud-fill')
        return clima
    return None


def index(request):
    # TI INFORMA
    ti_informa = TiInforma.objects.filter(ativo=True).order_by("ordem")

    # CLIMA
    clima_lista = []
    for c in CIDADES:
        clima = obter_clima(c['codigo'], c['uf'])
        if clima:
            clima_lista.append(clima)

    
    # QUADRO
    quadros = Quadro.objects.all()


    # ADMITIDOS
    hoje = date.today()
    admitidos_mes = Admitido.objects.filter(data_admissao__month=hoje.month, data_admissao__year=hoje.year)

    # PROMOÇÃO
    promocoes_mes = Promocao.objects.filter(
        data_promocao__month=hoje.month,
        data_promocao__year=hoje.year
    )

    contexto = {
        "ti_informa": ti_informa,
        "clima_lista": clima_lista,
        "quadros": quadros,
        "admitidos_mes": admitidos_mes,
        "promocoes_mes": promocoes_mes,
    }

    return render (request, 'index.html', contexto)


def etica_compliance(request):
    return render (request, 'etica_compliance.html')


# SERVIÇOS STATUS

FLUIG_URL = "http://fluig.totvs.com/healthCheck"
MEU_RH_URL = "http://rm.eletrodataengenharia.com.br:8082/web/app/RH/PortalMeuRH/"
NIMBI_URL = "https://app.nimbi.com.br"

def status_servicos(request):
    status = {}

    # FLUIG
    try:
        r = requests.get(FLUIG_URL, timeout=5)
        if r.status_code == 200:
            status["fluig"] = {"texto": "Ativo", "classe": "status-ok"}
        else:
            status["fluig"] = {"texto": "Oscilando", "classe": "status-warning"}
    except requests.exceptions.RequestException:
        status["fluig"] = {"texto": "Inativo", "classe": "status-error"}

    # MEU RH
    try:
        r = requests.get(MEU_RH_URL, timeout=5)
        if r.status_code == 200:
            status["meu_rh"] = {"texto": "Ativo", "classe": "status-ok"}
        else:
            status["meu_rh"] = {"texto": "Oscilando", "classe": "status-warning"}
    except requests.exceptions.RequestException:
        status["meu_rh"] = {"texto": "Inativo", "classe": "status-error"}

    # NIMBI
    try:
        r = requests.get(NIMBI_URL, timeout=5)
        if r.status_code == 200:
            status["nimbi"] = {"texto": "Ativo", "classe": "status-ok"}
        else:
            status["nimbi"] = {"texto": "Oscilando", "classe": "status-warning"}
    except requests.exceptions.RequestException:
        status["nimbi"] = {"texto": "Inativo", "classe": "status-error"}

    return JsonResponse(status)
    

