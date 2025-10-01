// JavaScript principal pour le site web

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des composants
    initializeComponents();
    
    // Gestion des messages flash
    handleFlashMessages();
    
    // Gestion des formulaires
    handleFormValidation();
    
    // Gestion des animations
    handleAnimations();
});

// Initialisation des composants
function initializeComponents() {
    console.log('Initialisation des composants...');
    
    // Initialiser les tooltips Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialiser les popovers Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Gestion des messages flash
function handleFlashMessages() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(function(alert) {
        // Auto-masquer les alertes après 5 secondes
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// Gestion de la validation des formulaires
function handleFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        });
    });
}

// Gestion des animations
function handleAnimations() {
    // Animation d'apparition des cartes
    const cards = document.querySelectorAll('.card');
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    });
    
    cards.forEach(function(card) {
        observer.observe(card);
    });
}

// Fonction pour tester l'API
function testAPI() {
    const button = event.target;
    const originalText = button.textContent;
    
    // Désactiver le bouton et afficher un spinner
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Chargement...';
    
    fetch('/api/hello')
        .then(response => response.json())
        .then(data => {
            document.getElementById('api-result').innerHTML = 
                '<div class="alert alert-success alert-dismissible fade show" role="alert">' +
                data.message +
                '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
                '</div>';
        })
        .catch(error => {
            document.getElementById('api-result').innerHTML = 
                '<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
                'Erreur: ' + error +
                '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
                '</div>';
        })
        .finally(() => {
            // Réactiver le bouton
            button.disabled = false;
            button.textContent = originalText;
        });
}

// Fonction pour copier du texte dans le presse-papiers
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Texte copié dans le presse-papiers!', 'success');
    }).catch(function(err) {
        console.error('Erreur lors de la copie: ', err);
        showToast('Erreur lors de la copie', 'error');
    });
}

// Fonction pour afficher des toasts
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div class="toast" id="${toastId}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <strong class="me-auto">Notification</strong>
                <small class="text-muted">maintenant</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Supprimer le toast du DOM après qu'il soit caché
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Créer le conteneur de toasts s'il n'existe pas
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

// Fonction pour formater les dates
function formatDate(date) {
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(date).toLocaleDateString('fr-FR', options);
}

// Fonction pour valider les emails
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Fonction pour valider les numéros de téléphone français
function validatePhone(phone) {
    const re = /^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$/;
    return re.test(phone);
}

// Fonction pour faire défiler vers le haut
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Ajouter un bouton "retour en haut" si la page est longue
function addScrollToTopButton() {
    if (window.scrollY > 300) {
        if (!document.getElementById('scroll-to-top')) {
            const button = document.createElement('button');
            button.id = 'scroll-to-top';
            button.className = 'btn btn-primary position-fixed bottom-0 end-0 m-3';
            button.style.zIndex = '1000';
            button.innerHTML = '↑';
            button.title = 'Retour en haut';
            button.onclick = scrollToTop;
            document.body.appendChild(button);
        }
    } else {
        const button = document.getElementById('scroll-to-top');
        if (button) {
            button.remove();
        }
    }
}

// Écouter le scroll pour le bouton "retour en haut"
window.addEventListener('scroll', addScrollToTopButton);

// Fonction pour gérer les liens externes
function handleExternalLinks() {
    const links = document.querySelectorAll('a[href^="http"]');
    links.forEach(link => {
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
    });
}

// Initialiser la gestion des liens externes
handleExternalLinks();

// Fonction pour gérer la navigation active
function setActiveNavigation() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Initialiser la navigation active
setActiveNavigation();

// Export des fonctions pour utilisation globale
window.testAPI = testAPI;
window.copyToClipboard = copyToClipboard;
window.showToast = showToast;
window.formatDate = formatDate;
window.validateEmail = validateEmail;
window.validatePhone = validatePhone;
window.scrollToTop = scrollToTop;
