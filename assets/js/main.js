document.addEventListener('DOMContentLoaded', () => {

    // Preloader
    const preloader = document.getElementById('preloader');
    if (preloader) {
        setTimeout(() => {
            preloader.style.opacity = '0';
            setTimeout(() => {
                preloader.style.display = 'none';
            }, 500);
        }, 1500); // simulate loading time
    }

    // Theme Toggle
    const themeToggleBtn = document.getElementById('theme-toggle');
    const rootElement = document.documentElement;
    const currentTheme = localStorage.getItem('theme') || 'light';

    if (currentTheme === 'dark') {
        rootElement.setAttribute('data-theme', 'dark');
        if (themeToggleBtn) themeToggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        if (themeToggleBtn) themeToggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            let theme = rootElement.getAttribute('data-theme');
            if (theme === 'dark') {
                rootElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                themeToggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
            } else {
                rootElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                themeToggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
            }
        });
    }

    // Navbar Scroll Effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Back to Top Button
    const backTopBtn = document.getElementById('back-top-btn');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backTopBtn.classList.add('show');
        } else {
            backTopBtn.classList.remove('show');
        }
    });
    if (backTopBtn) {
        backTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Chatbot Toggle
    const chatbotToggleBtn = document.getElementById('chatbot-toggle-btn');
    const chatbotWidget = document.getElementById('chatbot-widget');
    const chatbotClose = document.getElementById('chatbot-close');

    if (chatbotToggleBtn && chatbotWidget && chatbotClose) {
        chatbotToggleBtn.addEventListener('click', () => {
            chatbotWidget.classList.add('open');
            chatbotToggleBtn.style.display = 'none';
        });
        chatbotClose.addEventListener('click', () => {
            chatbotWidget.classList.remove('open');
            setTimeout(() => {
                chatbotToggleBtn.style.display = 'flex';
            }, 400);
        });
    }

    // Schedule Callback Toggle
    const callbackToggleBtn = document.getElementById('callback-toggle-btn');
    const callbackWidget = document.getElementById('callback-widget');
    const callbackClose = document.getElementById('callback-close');

    if (callbackToggleBtn && callbackWidget && callbackClose) {
        callbackToggleBtn.addEventListener('click', () => {
            callbackWidget.classList.add('open');
            callbackToggleBtn.style.display = 'none';
        });
        callbackClose.addEventListener('click', () => {
            callbackWidget.classList.remove('open');
            setTimeout(() => {
                callbackToggleBtn.style.display = 'flex';
            }, 400);
        });
    }

    // Hero Swiper Initialization
    if (document.querySelector('.hero-swiper')) {
        const heroSwiper = new Swiper('.hero-swiper', {
            loop: true,
            effect: 'fade',
            speed: 1500,
            autoplay: { delay: 5000, disableOnInteraction: false },
            pagination: { el: '.swiper-pagination', clickable: true },
            navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
        });
    }

    // Testimonial Swiper Initialization
    if (document.querySelector('.testimonial-swiper')) {
        const testimonialSwiper = new Swiper('.testimonial-swiper', {
            loop: true,
            speed: 1000,
            autoplay: { delay: 4000, disableOnInteraction: false },
            pagination: { el: '.swiper-pagination', clickable: true },
        });
    }

    // Smooth Scroll for Nav Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({ top: target.offsetTop - 80, behavior: 'smooth' });
            }
        });
    });

    // GSAP Scroll Animations
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);

        // Fade Up Elements
        gsap.utils.toArray('.gsap-fade-up').forEach(element => {
            gsap.fromTo(element, 
                { y: 50, opacity: 0 },
                {
                    y: 0, opacity: 1, duration: 1, ease: "power3.out",
                    scrollTrigger: { trigger: element, start: "top 85%", toggleActions: "play none none reverse" }
                }
            );
        });

        // Stagger Cards
        gsap.utils.toArray('.gsap-stagger-container').forEach(container => {
            const cards = container.querySelectorAll('.gsap-stagger-item');
            if (cards.length > 0) {
                gsap.fromTo(cards, 
                    { y: 50, opacity: 0 },
                    {
                        y: 0, opacity: 1, duration: 0.8, stagger: 0.15, ease: "power3.out",
                        scrollTrigger: { trigger: container, start: "top 80%", toggleActions: "play none none reverse" }
                    }
                );
            }
        });

        // Zoom In Elements
        gsap.utils.toArray('.gsap-zoom-in').forEach(element => {
            gsap.fromTo(element, 
                { scale: 0.8, opacity: 0 },
                {
                    scale: 1, opacity: 1, duration: 1, ease: "back.out(1.7)",
                    scrollTrigger: { trigger: element, start: "top 85%", toggleActions: "play none none reverse" }
                }
            );
        });
    }

    // Search Overlay Toggle
    const searchBtn = document.getElementById('navbarSearchBtn');
    const searchOverlay = document.getElementById('search-overlay');
    const searchClose = document.getElementById('searchClose');
    
    if (searchBtn && searchOverlay && searchClose) {
        searchBtn.addEventListener('click', (e) => {
            e.preventDefault();
            searchOverlay.classList.add('open');
        });
        searchClose.addEventListener('click', () => {
            searchOverlay.classList.remove('open');
        });
    }
});
