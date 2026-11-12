from django.contrib import admin
import csv
from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone

from .models import Projeto, Certificado, Contato, MembroEquipe, Acesso

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'atualizado_em')
    search_fields = ('nome',)

@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'projeto', 'emitido_em')
    search_fields = ('nome', 'projeto__nome')

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'criado_em')
    search_fields = ('nome', 'email')

@admin.register(MembroEquipe)
class MembroEquipeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')
    search_fields = ('nome', 'email', 'telefone')


PERIODOS = {'1': 'Hoje', '7': '7 dias', '30': '30 dias', '90': '90 dias', '365': '1 ano'}


@admin.register(Acesso)
class AcessoAdmin(admin.ModelAdmin):
    list_display = ('data', 'ip', 'pais', 'caminho', 'origem', 'dispositivo', 'navegador', 'sistema', 'robo')
    list_filter = ('robo', 'dispositivo', 'navegador', 'sistema', 'pais', 'data')
    search_fields = ('ip', 'caminho', 'origem', 'user_agent')
    date_hierarchy = 'data'
    list_per_page = 100
    change_list_template = 'admin/pages/acesso/change_list.html'

    # Os acessos são gravados automaticamente; ninguém cria/edita à mão.
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_urls(self):
        extras = [
            path('relatorio/', self.admin_site.admin_view(self.relatorio), name='pages_acesso_relatorio'),
            path('relatorio/csv/', self.admin_site.admin_view(self.relatorio_csv), name='pages_acesso_relatorio_csv'),
        ]
        return extras + super().get_urls()

    @staticmethod
    def _periodo(request):
        dias = request.GET.get('dias', '30')
        if dias not in PERIODOS:
            dias = '30'
        hoje = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
        inicio = hoje - timedelta(days=int(dias) - 1)
        incluir_robos = request.GET.get('robos') == '1'
        qs = Acesso.objects.filter(data__gte=inicio)
        if not incluir_robos:
            qs = qs.filter(robo=False)
        return dias, inicio, incluir_robos, qs

    @staticmethod
    def _ranking(qs, campo, limite=10, vazio='(direto / desconhecido)'):
        linhas = list(qs.values(campo).annotate(total=Count('id')).order_by('-total')[:limite])
        maior = linhas[0]['total'] if linhas else 1
        return [
            {'nome': l[campo] or vazio, 'total': l['total'], 'pct': round(l['total'] * 100 / maior)}
            for l in linhas
        ]

    def relatorio(self, request):
        dias, inicio, incluir_robos, qs = self._periodo(request)

        por_dia = list(
            qs.annotate(dia=TruncDate('data')).values('dia')
            .annotate(total=Count('id'), visitantes=Count('ip', distinct=True)).order_by('dia')
        )
        maior_dia = max((d['total'] for d in por_dia), default=1)
        for d in por_dia:
            d['pct'] = round(d['total'] * 100 / maior_dia)

        contexto = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'title': 'Relatório de acessos',
            'periodos': PERIODOS,
            'dias': dias,
            'inicio': inicio,
            'incluir_robos': incluir_robos,
            'total': qs.count(),
            'visitantes': qs.values('ip').distinct().count(),
            'robos': Acesso.objects.filter(data__gte=inicio, robo=True).count(),
            'por_dia': por_dia,
            'paginas': self._ranking(qs, 'caminho', vazio='/'),
            'origens': self._ranking(qs, 'origem'),
            'paises': self._ranking(qs, 'pais', vazio='(sem informação)'),
            'dispositivos': self._ranking(qs, 'dispositivo'),
            'navegadores': self._ranking(qs, 'navegador'),
            'sistemas': self._ranking(qs, 'sistema'),
            'visitantes_top': list(
                qs.values('ip', 'pais').annotate(total=Count('id')).order_by('-total')[:15]
            ),
            'ultimos': qs[:30],
            'url_csv': reverse('admin:pages_acesso_relatorio_csv'),
        }
        return TemplateResponse(request, 'admin/pages/acesso/relatorio.html', contexto)

    def relatorio_csv(self, request):
        dias, inicio, incluir_robos, qs = self._periodo(request)
        resposta = HttpResponse(content_type='text/csv; charset=utf-8')
        resposta['Content-Disposition'] = f'attachment; filename="acessos_{dias}dias.csv"'
        resposta.write('﻿')  # BOM para o Excel abrir os acentos certo
        escritor = csv.writer(resposta, delimiter=';')
        escritor.writerow(['Data', 'IP', 'País', 'Página', 'Veio de', 'Dispositivo', 'Navegador', 'Sistema', 'Robô', 'User-Agent'])
        for a in qs.iterator():
            escritor.writerow([
                timezone.localtime(a.data).strftime('%d/%m/%Y %H:%M:%S'), a.ip, a.pais, a.caminho,
                a.referencia, a.dispositivo, a.navegador, a.sistema, 'sim' if a.robo else 'não', a.user_agent,
            ])
        return resposta
