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

