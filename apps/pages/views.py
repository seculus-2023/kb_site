from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse, Http404
from .models import Projeto, Contato , MembroEquipe
import logging

logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    return render(request, 'index.html')

def contato(request):
    if request.method == 'POST':
        nome = (request.POST.get('nome') or '').strip()[:100]
        email = (request.POST.get('email') or '').strip()
        telefone = (request.POST.get('telefone') or '').strip()[:20]
        mensagem = (request.POST.get('mensagem') or '').strip()
        if nome and email and mensagem:
            Contato.objects.create(
                nome=nome,
                email=email,
                telefone=telefone,
                mensagem=mensagem
            )
            # Avisa por e-mail. A mensagem já ficou salva no banco (admin),
            # então uma falha no envio não deve aparecer como erro para o visitante.
            try:
                send_mail(
                    subject=f'Novo contato de {nome}',
                    message=f'Nome: {nome}\nE-mail: {email}\nTelefone: {telefone}\nMensagem: {mensagem}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['arpjunior40@gmail.com'],
                    fail_silently=False,
                )
            except Exception:
                logger.exception('Falha ao enviar e-mail do formulário de contato')
            messages.success(request, 'Mensagem enviada com sucesso! Em breve entraremos em contato.')
            return redirect('contato')
        else:
            messages.error(request, 'Preencha todos os campos obrigatórios.')
    return render(request, 'contato.html')

def equipe(request):
    return render(request, 'equipe.html')

def valores(request):
    return render(request, 'valores.html')

def historia(request):
    return render(request, 'historia.html')

def sistemas(request):
    projetos = Projeto.objects.filter(ativo=True)
    return render(request, 'sistemas.html', {'projetos': projetos})

def projetos(request):
    projetos = Projeto.objects.filter(ativo=True)
    return render(request, 'projetos.html', {'projetos': projetos})

def politica(request):
    return render(request, 'politica.html')

def agro(request):
    return render(request, 'agro.html')

def bolsatrader(request):
    return render(request, 'bolsatrader.html')

def seletivo(request):
    return render(request, 'seletivo.html')

def alvara(request):
    return render(request, 'alvara.html')

def membros(request):
    membros = MembroEquipe.objects.all()
    return render(request, 'membros.html', {'equipe': membros})


# ===== PWA (aplicativo instalável) =====

def instalar_app(request):
    """Passo a passo para instalar o site como aplicativo no computador ou celular."""
    return render(request, 'instalar.html')


def offline(request):
    """Tela mostrada pelo Service Worker quando não há internet."""
    return render(request, 'offline_site.html')


def service_worker(request):
    """
    Serve o Service Worker na raiz do site (/sw.js), para que ele controle
    todas as páginas (um service worker só controla as URLs dentro da pasta
    de onde é servido).
    """
    caminho = finders.find('js/service-worker.js')
    if not caminho:
        raise Http404('Service worker não encontrado.')
    with open(caminho, encoding='utf-8') as arquivo:
        conteudo = arquivo.read()
    resposta = HttpResponse(conteudo, content_type='application/javascript')
    resposta['Service-Worker-Allowed'] = '/'
    resposta['Cache-Control'] = 'no-cache'
    return resposta