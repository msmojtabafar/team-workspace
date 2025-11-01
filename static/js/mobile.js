// توابع مخصوص موبایل و PWA
class MobileApp {
    constructor() {
        this.isPWA = window.matchMedia('(display-mode: standalone)').matches;
        this.isMobile = this.detectMobile();
        this.init();
    }

    detectMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
            window.innerWidth <= 768;
    }

    init() {
        this.setupPWA();
        if (this.isMobile) {
            this.setupMobileUI();
        }
    }

    setupPWA() {
        // ثبت Service Worker
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/js/service-worker.js')
                .then(registration => {
                    console.log('Service Worker registered:', registration);
                })
                .catch(error => {
                    console.log('Service Worker registration failed:', error);
                });
        }

        // مدیریت نصب PWA
        let deferredPrompt;
        const installButton = document.getElementById('install-pwa');

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            
            if (installButton) {
                installButton.style.display = 'block';
                installButton.addEventListener('click', () => {
                    deferredPrompt.prompt();
                    deferredPrompt.userChoice.then((choiceResult) => {
                        if (choiceResult.outcome === 'accepted') {
                            console.log('User accepted install');
                        }
                        deferredPrompt = null;
                    });
                });
            }
        });

        window.addEventListener('appinstalled', () => {
            console.log('PWA installed');
            if (installButton) {
                installButton.style.display = 'none';
            }
        });
    }

    setupMobileUI() {
        this.addMobileNavigation();
        this.enhanceTouchInteractions();
    }

    addMobileNavigation() {
        const mobileNav = document.createElement('nav');
        mobileNav.className = 'mobile-nav safe-area-bottom';
        mobileNav.innerHTML = `
            <div class="mobile-nav-grid">
                <a href="/dashboard/" class="mobile-nav-item" data-route="dashboard">
                    <span class="mobile-nav-icon">📊</span>
                    <span>داشبورد</span>
                </a>
                <a href="/calendar/" class="mobile-nav-item" data-route="calendar">
                    <span class="mobile-nav-icon">📅</span>
                    <span>تقویم</span>
                </a>
                <a href="/projects/" class="mobile-nav-item" data-route="projects">
                    <span class="mobile-nav-icon">📂</span>
                    <span>پروژه‌ها</span>
                </a>
                <a href="/notifications/" class="mobile-nav-item" data-route="notifications">
                    <span class="mobile-nav-icon">🔔</span>
                    <span>اعلان‌ها</span>
                </a>
                <button class="mobile-nav-item" onclick="mobileApp.toggleMenu()">
                    <span class="mobile-nav-icon">☰</span>
                    <span>منو</span>
                </button>
            </div>
        `;

        document.body.appendChild(mobileNav);
    }

    enhanceTouchInteractions() {
        // اضافه کردن hover effects برای touch
        document.addEventListener('touchstart', function() {}, {passive: true});
        
        // بهبود تجربه لمسی
        document.querySelectorAll('button, a, input').forEach(element => {
            element.classList.add('touch-target');
        });
    }

    toggleMenu() {
        const menu = document.getElementById('mobile-menu');
        if (menu) {
            menu.remove();
        } else {
            this.createMobileMenu();
        }
    }

    createMobileMenu() {
        const menu = document.createElement('div');
        menu.id = 'mobile-menu';
        menu.className = 'fixed inset-0 bg-black bg-opacity-50 z-40';
        menu.innerHTML = `
            <div class="fixed bottom-0 left-0 right-0 bg-white rounded-t-2xl p-6">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-lg font-bold">منو</h3>
                    <button onclick="mobileApp.toggleMenu()" class="text-2xl">×</button>
                </div>
                <div class="space-y-4">
                    <a href="/dashboard/" class="block p-3 bg-gray-100 rounded-lg" onclick="mobileApp.toggleMenu()">📊 داشبورد</a>
                    <a href="/projects/" class="block p-3 bg-gray-100 rounded-lg" onclick="mobileApp.toggleMenu()">📂 پروژه‌ها</a>
                    <a href="/calendar/" class="block p-3 bg-gray-100 rounded-lg" onclick="mobileApp.toggleMenu()">📅 تقویم</a>
                    <a href="/notifications/" class="block p-3 bg-gray-100 rounded-lg" onclick="mobileApp.toggleMenu()">🔔 اعلان‌ها</a>
                    <a href="/admin/" class="block p-3 bg-gray-100 rounded-lg" onclick="mobileApp.toggleMenu()">⚙️ مدیریت</a>
                    <a href="/accounts/logout/" class="block p-3 bg-red-100 text-red-700 rounded-lg" onclick="mobileApp.toggleMenu()">🚪 خروج</a>
                </div>
            </div>
        `;

        menu.addEventListener('click', (e) => {
            if (e.target === menu) {
                this.toggleMenu();
            }
        });

        document.body.appendChild(menu);
    }
}

// مقداردهی اولیه اپ موبایل
const mobileApp = new MobileApp();

    createMobileMenu() {
        const menu = document.createElement('div');
        menu.id = 'mobile-menu';
        menu.className = 'fixed inset-0 bg-black bg-opacity-50 z-40';
        menu.innerHTML = `
            <div class="fixed bottom-0 left-0 right-0 bg-white rounded-t-2xl p-6">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-lg font-bold">منو</h3>
                    <button onclick="mobileApp.toggleMenu()" class="text-2xl">×</button>
                </div>
                <div class="space-y-4">
                    <a href="/dashboard/" class="block p-3 bg-gray-100 rounded-lg" onclick="mobileApp.toggleMenu()">📊 داشبورد</a>
                    <a href="/projects/" class="block p-3 bg-gray-100 rounded-lg" onclick="mobileApp.toggleMenu()">📂 پروژه‌ها</a>
                    <a href="/calendar/" class="block p-3 bg-gray-100 rounded-lg" onclick="mobileApp.toggleMenu()">📅 تقویم</a>
                    <a href="/notifications/" class="block p-3 bg-gray-100 rounded-lg" onclick="mobileApp.toggleMenu()">🔔 اعلان‌ها</a>
                    <a href="/admin/" class="block p-3 bg-gray-100 rounded-lg" onclick="mobileApp.toggleMenu()">⚙️ مدیریت</a>
                    <form method="post" action="/accounts/logout/" class="block">
                        {% csrf_token %}
                        <button type="submit" class="w-full text-right p-3 bg-red-100 text-red-700 rounded-lg" onclick="return confirm('آیا مطمئن هستید؟')">
                            🚪 خروج
                        </button>
                    </form>
                </div>
            </div>
        `;

        // اضافه کردن CSRF token به فرم logout
        const csrfToken = this.getCSRFToken();
        const logoutForm = menu.querySelector('form');
        if (logoutForm && csrfToken) {
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrfToken;
            logoutForm.appendChild(csrfInput);
        }

        menu.addEventListener('click', (e) => {
            if (e.target === menu) {
                this.toggleMenu();
            }
        });

        document.body.appendChild(menu);
    }

    // دریافت CSRF Token
    getCSRFToken() {
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfInput ? csrfInput.value : '';
    }
