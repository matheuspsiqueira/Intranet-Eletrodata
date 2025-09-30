from django.shortcuts import render
from .models import TiInforma
import requests


# CLIMA
API_KEY = '83994d6e956353c87b84ed10a6bd752f'

CIDADES = [
    {'nome': 'Rio de Janeiro', 'uf': 'RJ', 'codigo': 'Rio de Janeiro,BR'},
    {'nome': 'São Paulo', 'uf': 'SP', 'codigo': 'São Paulo,BR'},
    {'nome': 'Salvador', 'uf': 'BA', 'codigo': 'Salvador,BR'},
]


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

    contexto = {
        "ti_informa": ti_informa,
        "clima_lista": clima_lista,
    }

    return render (request, 'index.html', contexto)


def etica_compliance(request):
    return render (request, 'etica_compliance.html')
