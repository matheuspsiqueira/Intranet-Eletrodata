from django.contrib import admin
from .models import TiInforma, Quadro, Admitido, Promocao

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

@admin.register(Promocao)
class PromocaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo_anterior', 'novo_cargo', 'data_promocao')
    list_filter = ('data_promocao', 'novo_cargo')
    search_fields = ('nome', 'novo_cargo')