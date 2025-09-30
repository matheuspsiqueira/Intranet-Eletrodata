from django.db import models
from ckeditor.fields import RichTextField

class TiInforma(models.Model):
    titulo = models.CharField("Título", max_length=200, blank=True, null=True)
    descricao = RichTextField("Descrição")
    imagem = models.ImageField("Imagem", upload_to="ti_informa/")
    ativo = models.BooleanField("Ativo", default=True)
    ordem = models.PositiveIntegerField("Ordem", default=0)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["ordem", "-criado_em"]

    def __str__(self):
        return self.titulo or f"TI Informa #{self.id}"
