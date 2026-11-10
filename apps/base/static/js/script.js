document.addEventListener('DOMContentLoaded', function () {
    const dropdownToggles = document.querySelectorAll('.navbar .nav-item.dropdown > .nav-link.dropdown-toggle');

    dropdownToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function (event) {
            event.preventDefault();

            const parentDropdown = this.closest('.nav-item.dropdown');
            const menu = parentDropdown ? parentDropdown.querySelector('.dropdown-menu') : null;
            const shouldOpen = !parentDropdown.classList.contains('show');

            document.querySelectorAll('.navbar .nav-item.dropdown.show').forEach(function (openDropdown) {
                if (openDropdown !== parentDropdown) {
                    openDropdown.classList.remove('show');
                    const openMenu = openDropdown.querySelector('.dropdown-menu');
                    if (openMenu) {
                        openMenu.classList.remove('show');
                    }
                }
            });

            if (parentDropdown) {
                parentDropdown.classList.toggle('show', shouldOpen);
            }
            if (menu) {
                menu.classList.toggle('show', shouldOpen);
            }
        });
    });

    document.addEventListener('click', function (event) {
        if (!event.target.closest('.navbar .nav-item.dropdown')) {
            document.querySelectorAll('.navbar .nav-item.dropdown.show').forEach(function (dropdown) {
                dropdown.classList.remove('show');
                const menu = dropdown.querySelector('.dropdown-menu');
                if (menu) {
                    menu.classList.remove('show');
                }
            });
        }
    });
});

// Menu futurista: deixa a navbar mais sólida ao rolar a página
(function () {
    const nav = document.querySelector('.navbar-futurista');
    if (!nav) return;
    const onScroll = function () {
        nav.classList.toggle('nf-scrolled', window.scrollY > 20);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
})();

// Animação de entrada: elementos com a classe "revelar" aparecem ao rolar
(function () {
    const itens = document.querySelectorAll('.revelar');
    if (!itens.length) return;
    if (!('IntersectionObserver' in window)) {
        itens.forEach(function (el) { el.classList.add('visivel'); });
        return;
    }
    const observador = new IntersectionObserver(function (entradas) {
        entradas.forEach(function (entrada) {
            if (entrada.isIntersecting) {
                entrada.target.classList.add('visivel');
                observador.unobserve(entrada.target);
            }
        });
    }, { threshold: 0.12 });
    itens.forEach(function (el) { observador.observe(el); });
})();
