"""
Registro de acessos ao site (quem visitou, quando, qual página, de onde veio).

O AcessoMiddleware grava um registro de Acesso para cada página HTML aberta.
Arquivos estáticos, mídia, admin e o service worker não são registrados.
O relatório fica no admin: /admin/pages/acesso/relatorio/
"""
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

IGNORAR_PREFIXOS = ('/admin', '/static', '/media', '/sw.js', '/favicon', '/manifest', '/robots.txt')

PALAVRAS_ROBO = ('bot', 'crawl', 'spider', 'slurp', 'facebookexternalhit', 'preview',
                 'curl', 'wget', 'python-requests', 'httpx', 'headless', 'monitor',
                 'scan', 'go-http-client', 'java/', 'okhttp', 'axios')


def ip_do_visitante(request):
    """IP real do visitante. O site fica atrás da Cloudflare e do Caddy,
    então REMOTE_ADDR é sempre 127.0.0.1; o IP real vem nos cabeçalhos."""
    meta = request.META
    remoto = meta.get('REMOTE_ADDR', '')
    if remoto in ('127.0.0.1', '::1'):  # só confia nos cabeçalhos vindos do proxy local
        ip = meta.get('HTTP_CF_CONNECTING_IP') or ''
        if not ip:
            ip = (meta.get('HTTP_X_FORWARDED_FOR') or '').split(',')[0]
        ip = ip.strip()
        if ip:
            return ip
    return remoto or None


def analisar_user_agent(ua):
    """Classificação simples (sem biblioteca externa) de navegador/sistema/dispositivo."""
    u = ua.lower()
    robo = not ua or any(p in u for p in PALAVRAS_ROBO)

    if 'edg/' in u:
        navegador = 'Edge'
    elif 'opr/' in u or 'opera' in u:
        navegador = 'Opera'
    elif 'samsungbrowser' in u:
        navegador = 'Samsung Internet'
    elif 'firefox' in u or 'fxios' in u:
        navegador = 'Firefox'
    elif 'chrome' in u or 'crios' in u:
        navegador = 'Chrome'
    elif 'safari' in u:
        navegador = 'Safari'
    else:
        navegador = 'Outro'

    if 'android' in u:
        sistema = 'Android'
    elif 'iphone' in u or 'ipad' in u or 'ipod' in u:
        sistema = 'iOS'
    elif 'windows' in u:
        sistema = 'Windows'
    elif 'mac os' in u or 'macintosh' in u:
        sistema = 'macOS'
    elif 'linux' in u:
        sistema = 'Linux'
    else:
        sistema = 'Outro'

    if robo:
        dispositivo = 'Robô'
    elif 'ipad' in u or 'tablet' in u or ('android' in u and 'mobile' not in u):
        dispositivo = 'Tablet'
    elif 'mobi' in u or 'iphone' in u:
        dispositivo = 'Celular'
    else:
        dispositivo = 'Computador'

    return navegador, sistema, dispositivo, robo


class AcessoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            if self._deve_registrar(request, response):
                self._registrar(request)
        except Exception:
            # Registrar acesso nunca pode derrubar o site.
            logger.exception('Falha ao registrar acesso')
        return response

    @staticmethod
    def _deve_registrar(request, response):
        if request.method != 'GET' or response.status_code != 200:
            return False
        if request.path.startswith(IGNORAR_PREFIXOS):
            return False
        if 'text/html' not in response.get('Content-Type', ''):
            return False
        # O service worker pré-carrega páginas para o modo offline; não é visita real.
        if request.headers.get('Service-Worker') or request.headers.get('Purpose') == 'prefetch':
            return False
        return True

    @staticmethod
    def _registrar(request):
        from .models import Acesso

        ua = request.META.get('HTTP_USER_AGENT', '')[:1000]
        navegador, sistema, dispositivo, robo = analisar_user_agent(ua)

        referencia = request.META.get('HTTP_REFERER', '')[:500]
        origem = ''
        if referencia:
            host = (urlparse(referencia).hostname or '').lower()
            if host.startswith('www.'):
                host = host[4:]
            proprio = request.get_host().split(':')[0].lower()
            if proprio.startswith('www.'):
                proprio = proprio[4:]
            if host and host != proprio:
                origem = host[:200]

        caminho = request.get_full_path()[:500]
        Acesso.objects.create(
            ip=ip_do_visitante(request),
            pais=(request.META.get('HTTP_CF_IPCOUNTRY') or '')[:2].upper(),
            caminho=caminho,
            referencia=referencia,
            origem=origem,
            user_agent=ua,
            navegador=navegador,
            sistema=sistema,
            dispositivo=dispositivo,
            robo=robo,
        )
