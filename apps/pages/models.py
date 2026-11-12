from django.db import models

class Projeto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    logo = models.ImageField(upload_to='logos/')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Certificado(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='certificados')
    nome = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to='certificados/')
    emitido_em = models.DateField()
    imagem = models.ImageField(upload_to='certificados/img/', blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.projeto.nome})"

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True, null=True)
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} <{self.email}>"
class MembroEquipe(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)  
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    foto = models.ImageField(upload_to='membros_fotos/', blank=True, null=True)

    def __str__(self):
        return self.nome



class Acesso(models.Model):
    """Uma visita a uma página do site (gravada pelo AcessoMiddleware)."""
    data = models.DateTimeField(auto_now_add=True, db_index=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    pais = models.CharField('país', max_length=2, blank=True)
    caminho = models.CharField('página', max_length=500)
    referencia = models.CharField('veio de (URL)', max_length=500, blank=True)
    origem = models.CharField('veio de (site)', max_length=200, blank=True, db_index=True)
    user_agent = models.TextField(blank=True)
    navegador = models.CharField(max_length=30, blank=True)
    sistema = models.CharField(max_length=30, blank=True)
    dispositivo = models.CharField(max_length=20, blank=True)
    robo = models.BooleanField('robô', default=False, db_index=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'acesso'
        verbose_name_plural = 'acessos'

    def __str__(self):
        return f"{self.data:%d/%m/%Y %H:%M} {self.ip} {self.caminho}"
