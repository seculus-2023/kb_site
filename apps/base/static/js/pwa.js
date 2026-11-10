/*
 * Registro do Service Worker e controle dos botões "Instalar app" (PWA).
 */
(function () {
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      // Remove o service worker antigo do django-pwa (/serviceworker.js),
      // que não é mais servido, para ele não continuar controlando o site.
      navigator.serviceWorker.getRegistrations().then(function (registros) {
        registros.forEach(function (registro) {
          const ativo = registro.active || registro.waiting || registro.installing;
          if (ativo && ativo.scriptURL.indexOf("/serviceworker.js") !== -1) {
            registro.unregister();
          }
        });
      });

      navigator.serviceWorker.register("/sw.js").catch(function (erro) {
        console.warn("Falha ao registrar o Service Worker:", erro);
      });
    });

    // Quando uma versão nova do service worker assume, recarrega a página
    // uma única vez para página e service worker ficarem na mesma versão.
    let jaRecarregou = false;
    navigator.serviceWorker.addEventListener("controllerchange", function () {
      if (jaRecarregou) return;
      jaRecarregou = true;
      window.location.reload();
    });
  }

  // O navegador avisa (beforeinstallprompt) quando o site pode ser
  // instalado; só então os botões "Instalar app" aparecem.
  let eventoInstalacaoAdiado = null;
  const botoesInstalar = [
    document.getElementById("btn-instalar-pwa"),          // menu do topo
    document.getElementById("btn-instalar-pwa-flutuante"), // botão flutuante
    document.getElementById("btn-instalar-pwa-pagina"),    // tela "Instalar o aplicativo"
  ].filter(Boolean);

  window.addEventListener("beforeinstallprompt", function (evento) {
    evento.preventDefault();
    eventoInstalacaoAdiado = evento;
    botoesInstalar.forEach(function (botao) {
      botao.style.display = "inline-block";
    });
  });

  botoesInstalar.forEach(function (botao) {
    botao.addEventListener("click", function () {
      if (!eventoInstalacaoAdiado) return;
      botoesInstalar.forEach(function (b) { b.style.display = "none"; });
      eventoInstalacaoAdiado.prompt();
      eventoInstalacaoAdiado.userChoice.finally(function () {
        eventoInstalacaoAdiado = null;
      });
    });
  });

  window.addEventListener("appinstalled", function () {
    botoesInstalar.forEach(function (botao) {
      botao.style.display = "none";
    });
  });
})();
