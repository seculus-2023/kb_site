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

def clinica(request):
    return render(request, 'clinica.html')


# Certificados do fundador. Areas: genexus, dev, gestao, financas.
# Dados pessoais (RG, nascimento, filiacao) que aparecem em alguns
# certificados ficam de fora de proposito: a pagina e publica.
AREAS_CERTIFICADOS = [
    ('genexus', 'GeneXus e low-code', 'fas fa-cubes'),
    ('dev', 'Programação', 'fas fa-code'),
    ('gestao', 'Análise, processos e gestão', 'fas fa-diagram-project'),
    ('financas', 'Mercado financeiro', 'fas fa-chart-line'),
]

CERTIFICADOS = [
    {'ano': 2026, 'data': '10/11/2026', 'titulo': 'Bolsa de Valores: Aprenda a Investir em Ações', 'instituicao': 'Udemy', 'area': 'financas', 'horas': 4, 'url': 'https://ude.my/UC-7200d21e-e94a-4f91-9651-ebae4fe6b44d', 'codigo': 'UC-7200d21e-e94a-4f91-9651-ebae4fe6b44d'},
    {'ano': 2026, 'data': '02/11/2026', 'titulo': 'Central Depositária da B3', 'instituicao': 'B3 Educação', 'area': 'financas', 'horas': 1},
    {'ano': 2026, 'data': '22/10/2026', 'titulo': 'Investindo em Small Caps', 'instituicao': 'B3 Educação, Hub de Educação Financeira', 'area': 'financas', 'horas': 4},
    {'ano': 2024, 'data': '22/04/2024', 'titulo': 'Scrum Foundation Professional Certification (SFPC)', 'instituicao': 'CertiProf', 'area': 'gestao', 'codigo': 'ID 95853349', 'destaque': True},
    {'ano': 2023, 'data': 'Outubro de 2023', 'titulo': 'GeneXus 18 Senior Analyst', 'instituicao': 'GeneXus Training', 'area': 'genexus', 'nota': '80%', 'destaque': True},
    {'ano': 2022, 'data': 'Novembro de 2022', 'titulo': 'GeneXus 17 BPM Suite Lab', 'instituicao': 'GeneXus Training', 'area': 'genexus', 'nota': '93%'},
    {'ano': 2022, 'data': 'Novembro de 2022', 'titulo': 'GeneXus 17 for Mobile Lab', 'instituicao': 'GeneXus Training', 'area': 'genexus', 'nota': '89%'},
    {'ano': 2022, 'data': 'Novembro de 2022', 'titulo': 'GeneXus 17 for Students', 'instituicao': 'GeneXus Training', 'area': 'genexus', 'nota': '62%'},
    {'ano': 2020, 'data': '16/06/2020', 'titulo': 'Criando APIs robustas em C#', 'instituicao': 'Udemy', 'area': 'dev', 'horas': 9, 'url': 'https://ude.my/UC-7a683660-e943-44ad-99d4-00642d1766d8', 'codigo': 'UC-7a683660-e943-44ad-99d4-00642d1766d8'},
    {'ano': 2020, 'data': '09/06/2020', 'titulo': 'Ionic 5 do Zero até Publicação', 'instituicao': 'Udemy', 'area': 'dev', 'horas': 13, 'url': 'https://ude.my/UC-09e65827-7ad9-44d8-a8e2-5e219cde63fe', 'codigo': 'UC-09e65827-7ad9-44d8-a8e2-5e219cde63fe'},
    {'ano': 2019, 'data': '20/05/2019', 'titulo': 'Introdução ao PHP orientado a objetos', 'instituicao': 'Prof. Diego Mariano', 'area': 'dev', 'horas': 1, 'url': 'http://diegomariano.com/certificados', 'codigo': 'L876GX'},
    {'ano': 2019, 'data': '30/04/2019', 'titulo': 'Criação de Páginas de Internet Dinâmicas com PHP', 'instituicao': 'Prof. Diego Mariano', 'area': 'dev', 'horas': 2, 'url': 'http://diegomariano.com/certificados', 'codigo': 'C2U2MX'},
    {'ano': 2011, 'data': '15 a 19/08/2011', 'titulo': 'Ferramenta de desenvolvimento MAKER', 'instituicao': 'Softwell Solutions', 'area': 'genexus', 'horas': 40, 'local': 'Salvador/BA'},
    {'ano': 2010, 'data': '05/10/2010', 'titulo': 'Gestão de Processos', 'instituicao': 'SENAI Mato Grosso', 'area': 'gestao', 'horas': 20, 'local': 'Cuiabá/MT'},
    {'ano': 2010, 'data': 'Setembro de 2010', 'titulo': 'Analista Sênior GeneXus X Evolution 1', 'instituicao': 'Artech Consultores (GeneXus)', 'area': 'genexus', 'nota': '94%', 'local': 'São Paulo/SP', 'destaque': True},
    {'ano': 2010, 'data': '14/09/2010', 'titulo': 'Gestão de Processos (BPM)', 'instituicao': 'Fundação Bradesco, Escola Virtual', 'area': 'gestao', 'horas': 7},
    {'ano': 2009, 'data': '14 a 21/09/2009', 'titulo': 'Liderança e Motivação de Equipes', 'instituicao': 'SENAC Mato Grosso', 'area': 'gestao', 'horas': 16, 'local': 'Cuiabá/MT'},
    {'ano': 2008, 'data': '17 e 18/07/2008', 'titulo': 'Workshop de Gerenciamento Ágil de Projetos com Scrum', 'instituicao': 'Innovit e iuni Educacional', 'area': 'gestao', 'horas': 16},
    {'ano': 2007, 'data': '21 a 25/05/2007', 'titulo': 'Técnicas de Comunicação', 'instituicao': 'SEBRAE Mato Grosso', 'area': 'gestao', 'horas': 16, 'local': 'Cuiabá/MT'},
    {'ano': 2006, 'data': '04 a 15/12/2006', 'titulo': 'Introdução ao GeneXus 9.0 Java Web', 'instituicao': 'Ábaco Tecnologia de Informação', 'area': 'genexus', 'horas': 20, 'local': 'Cuiabá/MT'},
    {'ano': 2006, 'data': '23 a 27/10/2006', 'titulo': 'Introdução à UML', 'instituicao': 'Ábaco Tecnologia de Informação', 'area': 'gestao', 'horas': 20, 'local': 'Cuiabá/MT'},
    {'ano': 2006, 'data': '17 a 24/07/2006', 'titulo': 'Análise de Pontos de Função', 'instituicao': 'Ábaco Tecnologia de Informação', 'area': 'gestao', 'horas': 20, 'local': 'Cuiabá/MT'},
    {'ano': 1999, 'data': '05/11/1999', 'titulo': 'Progress: Application Development Environment', 'instituicao': 'Dual Software', 'area': 'dev', 'local': 'São José do Rio Preto/SP'},
    {'ano': 1999, 'data': '05/11/1999', 'titulo': 'Progress: PIP, Programming In Progress', 'instituicao': 'Dual Software', 'area': 'dev', 'local': 'São José do Rio Preto/SP'},
    {'ano': 1990, 'data': '30/06/1990', 'titulo': 'Programação COBOL', 'instituicao': 'PROANSI Informática', 'area': 'dev', 'local': 'São José do Rio Preto/SP'},
    {'ano': 1985, 'data': '1985', 'titulo': 'Curso de Informática, linguagem Basic (1º e 2º estágios)', 'instituicao': 'The Way Informática', 'area': 'dev', 'nota': 'média 7,0', 'local': 'São José do Rio Preto/SP'},
]


def certificados(request):
    nomes = {chave: (nome, icone) for chave, nome, icone in AREAS_CERTIFICADOS}
    lista = []
    for c in CERTIFICADOS:
        item = dict(c)
        item['area_nome'], item['area_icone'] = nomes[c['area']]
        lista.append(item)
    areas = [
        {'chave': chave, 'nome': nome, 'icone': icone,
         'total': sum(1 for c in CERTIFICADOS if c['area'] == chave)}
        for chave, nome, icone in AREAS_CERTIFICADOS
    ]
    anos = [c['ano'] for c in CERTIFICADOS]
    contexto = {
        'certificados': lista,
        'areas': areas,
        'total': len(CERTIFICADOS),
        'horas': sum(c.get('horas', 0) for c in CERTIFICADOS),
        'primeiro_ano': min(anos),
        'destaques': [c for c in lista if c.get('destaque')],
    }
    return render(request, 'certificados.html', contexto)

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