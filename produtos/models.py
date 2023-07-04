from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=50)
    preco = models.FloatField()

    def __str__(self) -> str:
        return self.nome
    
    def exibe_preco(self):
        return "{:.2f}".format(self.preco)