from django.contrib import admin
from .models import TiInforma, Quadro, Admitido

@admin.register(TiInforma)
class TiInformaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "ativo", "ordem", "criado_em")
    list_filter = ("ativo",)
    search_fields = ("titulo", "descricao")
    ordering = ("ordem",)

@admin.register(Quadro)
class QuadroAdmin(admin.ModelAdmin):
    list_display = ('posicao', 'titulo')
    list_editable = ('titulo',)

@admin.register(Admitido)
class AdmitidoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'data_admissao')
    list_filter = ('data_admissao', 'cargo')
    search_fields = ('nome', 'cargo')