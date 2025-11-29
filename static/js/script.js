// Weather App JavaScript

function searchCity(cityName) {
    const cityInput = document.getElementById('city');
    if (cityInput) {
        cityInput.value = cityName;
        cityInput.form.submit();
    }
}

// Add loading state to forms
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.7';
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span>Loading...</span>';
                
                // Re-enable after 5 seconds as fallback
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.style.opacity = '1';
                    submitBtn.innerHTML = originalText;
                }, 5000);
            }
        });
    });
    
    // Auto-focus on input fields
    const cityInput = document.getElementById('city');
    if (cityInput) {
        cityInput.focus();
    }
});

// Handle Enter key on example buttons
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.target.classList.contains('btn-example')) {
        e.target.click();
    }
});
