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


# QUADRO
class Quadro(models.Model):
    POSICOES = [
        (1, 'Quadro 1 (Grande à esquerda)'),
        (2, 'Quadro 2 (Retangular em cima à direita)'),
        (3, 'Quadro 3 (Quadrado pequeno à direita - esquerda)'),
        (4, 'Quadro 4 (Quadrado pequeno à direita - direita)'),
    ]

    posicao = models.PositiveSmallIntegerField(
        choices=POSICOES,
        unique=True,
        verbose_name="Posição do Quadro"
    )
    titulo = models.CharField(max_length=255, verbose_name="Título")
    imagem = models.ImageField(upload_to="quadros/", verbose_name="Imagem Normal")
    imagem_overlay = models.ImageField(
        upload_to="quadros/overlays/",
        verbose_name="Imagem para Overlay",
        blank=True,
        null=True
    )
    link = models.URLField(blank=True, null=True, verbose_name="Link (opcional)")

    def save(self, *args, **kwargs):
        # Se já existir um quadro na mesma posição, apaga antes de salvar o novo
        Quadro.objects.filter(posicao=self.posicao).exclude(pk=self.pk).delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_posicao_display()} - {self.titulo}"



# ADMITIDOS
class Admitido(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    cargo = models.CharField(max_length=255, verbose_name="Cargo")
    data_admissao = models.DateField(verbose_name="Data de Admissão")

    class Meta:
        ordering = ['data_admissao']  # ordena por data

    def __str__(self):
        return f"{self.nome} - {self.cargo}"
    

# PROMOÇÃO
class Promocao(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    cargo_anterior = models.CharField(max_length=255, verbose_name="Cargo Anterior", blank=True, null=True)
    novo_cargo = models.CharField(max_length=255, verbose_name="Novo Cargo")
    data_promocao = models.DateField(verbose_name="Data da Promoção")

    class Meta:
        ordering = ['data_promocao']

    def __str__(self):
        return f"{self.nome} → {self.novo_cargo}"