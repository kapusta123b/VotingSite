
document.addEventListener('DOMContentLoaded', () => {
    
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav ul li a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    const copyButtons = document.querySelectorAll('.btn-outline');
    copyButtons.forEach(btn => {
        if (btn.textContent.trim() === 'Copy Link') {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                navigator.clipboard.writeText(window.location.href).then(() => {
                    const originalText = btn.textContent;
                    btn.textContent = 'Copied!';
                    btn.style.color = 'var(--success)';
                    setTimeout(() => {
                        btn.textContent = originalText;
                        btn.style.color = '';
                    }, 2000);
                });
            });
        }
    });
});
