document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.employee-form-card');
    const dateNaissance = document.getElementById('id_date_naissance');
    const dateEmbauche = document.getElementById('id_date_embauche');
    const telephone = document.getElementById('id_telephone');

    form.addEventListener('submit', function(e) {
        let hasErrors = false;

        // Validation date de naissance
        if (dateNaissance.value) {
            const today = new Date().toISOString().split('T')[0];
            if (dateNaissance.value >= today) {
                showError(dateNaissance, "La date de naissance doit être dans le passé.");
                hasErrors = true;
            } else {
                clearError(dateNaissance);
            }
        }

        // Validation date d'embauche
        if (dateEmbauche.value) {
            const today = new Date().toISOString().split('T')[0];
            if (dateEmbauche.value > today) {
                showError(dateEmbauche, "La date d'embauche ne peut pas être dans le futur.");
                hasErrors = true;
            } else {
                clearError(dateEmbauche);
            }
        }

        // Validation téléphone
        if (telephone.value) {
            if (!/^\d{10}$/.test(telephone.value)) {
                showError(telephone, "Le numéro de téléphone doit contenir exactement 10 chiffres.");
                hasErrors = true;
            } else {
                clearError(telephone);
            }
        }

        if (hasErrors) {
            e.preventDefault();
            alert("Veuillez corriger les erreurs dans le formulaire.");
        }
    });

    function showError(field, message) {
        clearError(field);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
    }

    function clearError(field) {
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }
});