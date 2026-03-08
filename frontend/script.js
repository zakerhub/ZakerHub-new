document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Hero Text and Card Entrance Animation (On Load) ---
    const headline = document.getElementById('headline-text');
    const visualCard = document.getElementById('visual-card');

    // Split headline text into words for individual animation
    headline.innerHTML = headline.textContent.split(' ').map(word => 
        `<span style="display: inline-block; opacity: 0;">${word}</span>`
    ).join(' ');

    const words = headline.querySelectorAll('span');
    
    // Animate words in sequence
    words.forEach((word, index) => {
        setTimeout(() => {
            word.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
            word.style.opacity = '1';
            word.style.transform = 'translateY(0)';
        }, index * 80); // Stagger the animation
    });

    // Animate the Card (3D Tilt Reveal)
    setTimeout(() => {
        visualCard.querySelector('.card-mockup').style.transition = 'all 1s cubic-bezier(0.25, 0.46, 0.45, 0.94)'; 
        visualCard.querySelector('.card-mockup').style.opacity = '1';
        visualCard.querySelector('.card-mockup').style.transform = 'perspective(1000px) rotateY(0deg) scale(1)';
    }, 500); 

    // --- 2. Chart Value Animation (Simulating Live Data) ---
    const chartBars = document.querySelectorAll('.chart-bar');
    
    setTimeout(() => {
        chartBars.forEach(bar => {
            const originalHeight = bar.style.height; 
            bar.style.height = '10%'; 
            
            setTimeout(() => {
                bar.style.height = originalHeight; 
            }, 100);
        });
    }, 1200);


    // --- 3. Scroll-Based Fade-In Animation (Featurette and Curriculum Sections) ---
    const observerOptions = {
        root: null, 
        rootMargin: '0px',
        threshold: 0.1 
    };

    // Select all items that need to fade in on scroll
    const itemsToObserve = document.querySelectorAll('.feature-item, .curriculum-item');

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    itemsToObserve.forEach((item, index) => {
        // Apply staggered delay across all observed items
        item.style.transitionDelay = `${index * 0.15}s`;
        item.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(item);
    });

    // --- 4. Navbar Shadow on Scroll ---
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.boxShadow = '0 2px 10px var(--color-shadow)';
            navbar.style.backgroundColor = 'var(--color-white)';
        } else {
            navbar.style.boxShadow = 'none';
            navbar.style.backgroundColor = 'transparent';
        }
    });
});