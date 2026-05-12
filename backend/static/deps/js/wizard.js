document.addEventListener('DOMContentLoaded', () => {
    const openBtn = document.getElementById('open-poll-wizard');
    const closeBtn = document.getElementById('close-poll-wizard');
    const overlay = document.getElementById('poll-wizard-overlay');
    const body = document.body;

    if (!openBtn || !overlay) return;

    const toggleWizard = (show) => {
        if (show) {
            overlay.classList.add('active');
            body.style.overflow = 'hidden'; 
        } else {
            overlay.classList.remove('active');
            body.style.overflow = '';
            
            const url = new URL(window.location);
            url.searchParams.delete('wizard');
            url.searchParams.delete('refresh');
            window.history.replaceState({}, '', url);
        }
    };

    openBtn.addEventListener('click', (e) => {
        e.preventDefault();
        toggleWizard(true);
    });

    closeBtn?.addEventListener('click', () => toggleWizard(false));

    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) toggleWizard(false);
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && overlay.classList.contains('active')) {
            toggleWizard(false);
        }
    });
});
