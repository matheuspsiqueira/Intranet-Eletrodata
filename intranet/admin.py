from django.contrib import admin
from .models import TiInforma

@admin.register(TiInforma)
class TiInformaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "ativo", "ordem", "criado_em")
    list_filter = ("ativo",)
    search_fields = ("titulo", "descricao")
    ordering = ("ordem",)
