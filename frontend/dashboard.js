document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. Dashboard Element Entrance Animation ---
    // Select all cards and tasks that should animate
    const animatedElements = document.querySelectorAll('.animated-card, .animated-task');

    animatedElements.forEach((element, index) => {
        // Apply the animation keyframe
        element.style.animation = `fadeInSlideUp 0.6s ease-out forwards`;
        
        // Stagger the animation timing for a waterfall effect
        element.style.animationDelay = `${index * 0.08}s`;
        
        // Set initial opacity to 0 so the animation takes effect
        element.style.opacity = '0';
    });
    
    // --- 2. Live Meeting Highlight (Urgency) ---
    const meetingItem = document.querySelector('.meeting-item');
    const zoomLink = document.querySelector('.zoom-link');
    
    if (meetingItem && zoomLink) {
        // Simple blinking effect for "Starting in 15 mins"
        let isHighlighted = false;
        setInterval(() => {
            if (isHighlighted) {
                meetingItem.style.boxShadow = 'none';
            } else {
                // Highlight with a subtle green glow
                meetingItem.style.boxShadow = '0 0 10px rgba(0, 202, 78, 0.5)';
            }
            isHighlighted = !isHighlighted;
        }, 1500); // Toggle every 1.5 seconds for a soft pulse
    }
    
    // --- 3. Sidebar Active State Management ---
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            // Remove active class from all items
            navItems.forEach(i => i.classList.remove('active'));
            // Add active class to the clicked item
            e.currentTarget.classList.add('active');
        });
    });
});