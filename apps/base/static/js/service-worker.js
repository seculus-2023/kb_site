/*
 * Service Worker do site Seculus (PWA).
 *
 * Servido pela view pages.views.service_worker em /sw.js, para que o escopo
 * cubra o site inteiro (um service worker só controla as URLs dentro da
 * pasta de onde é servido).
 *
 * Estratégia:
 *   - Páginas: sempre da rede. Sem internet, mostra a tela /offline/.
 *   - Arquivos estáticos (CSS/JS/ícones): cache primeiro, atualizando em
 *     segundo plano.
 *   - Vídeos e outros arquivos grandes: não passam pelo cache (o navegador
 *     pede o vídeo em pedaços, e pedaços não podem ser guardados no cache).
 *
 * Ao mudar este arquivo, troque VERSAO_CACHE para os navegadores baixarem
 * a versão nova e apagarem o cache antigo.
 */

const VERSAO_CACHE = "seculus-v2";
const CACHE_SHELL = `${VERSAO_CACHE}-shell`;

const ARQUIVOS_APP_SHELL = [
  "/static/css/style.css",
  "/static/js/script.js",
  "/static/js/pwa.js",
  "/static/manifest.webmanifest",
  "/static/icons/icon-192.png",
  "/static/icons/icon-512.png",
  "/static/icons/icon-512-maskable.png",
  "/static/icons/apple-touch-icon.png",
  "/static/icons/favicon-32.png",
  "/static/icons/favicon-16.png",
  "/offline/",
];

self.addEventListener("install", (evento) => {
  evento.waitUntil(
    caches.open(CACHE_SHELL).then((cache) => cache.addAll(ARQUIVOS_APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (evento) => {
  evento.waitUntil(
    caches.keys().then((nomes) =>
      Promise.all(
        nomes
          // apaga versões antigas deste SW e o cache do django-pwa usado antes
          .filter((nome) => nome !== CACHE_SHELL && (nome.startsWith("seculus-") || nome.startsWith("django-pwa-")))
          .map((nome) => caches.delete(nome))
      )
    )
  );
  self.clients.claim();
});

function ehArquivoEstaticoCacheavel(url) {
  return (
    url.origin === self.location.origin &&
    url.pathname.startsWith("/static/") &&
    !/\.(mp4|webm|mov|pdf)$/i.test(url.pathname)
  );
}

self.addEventListener("fetch", (evento) => {
  const { request } = evento;
  if (request.method !== "GET") return; // nunca interceptar POST (formulário de contato etc.)

  const url = new URL(request.url);

  // Navegação de página: rede; sem internet, tela offline
  if (request.mode === "navigate") {
    evento.respondWith(
      fetch(request).catch(() =>
        caches.match("/offline/").then((resp) => resp || Response.error())
      )
    );
    return;
  }

  // Arquivos estáticos: cache primeiro, atualizando em segundo plano
  if (ehArquivoEstaticoCacheavel(url)) {
    evento.respondWith(
      caches.open(CACHE_SHELL).then((cache) =>
        cache.match(request).then((respostaCache) => {
          const buscaRede = fetch(request)
            .then((respostaRede) => {
              if (respostaRede.ok && respostaRede.status === 200) {
                cache.put(request, respostaRede.clone());
              }
              return respostaRede;
            })
            .catch(() => respostaCache);
          return respostaCache || buscaRede;
        })
      )
    );
    return;
  }

  // Demais requisições (mídia, admin, vídeo etc.): sempre da rede.
});
