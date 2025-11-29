// Weather Info App - Main JavaScript

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Weather Info App initialized');
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const cityInput = this.querySelector('input[name="city"]');
            if (cityInput) {
                const cityValue = cityInput.value.trim();
                
                // Validate city name
                if (!cityValue) {
                    e.preventDefault();
                    showNotification('Please enter a city name', 'warning');
                    return false;
                }
                
                // Check for valid characters
                const validPattern = /^[a-zA-Z0-9\s\-,.]+$/;
                if (!validPattern.test(cityValue)) {
                    e.preventDefault();
                    showNotification('Please enter a valid city name (letters, numbers, spaces, hyphens, commas, and periods only)', 'warning');
                    return false;
                }
                
                // Trim and set the value
                cityInput.value = cityValue;
            }
        });
    });
});

// Show notification function
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

// Fetch weather data via API (for future enhancements)
async function fetchWeatherAPI(city) {
    try {
        const response = await fetch(`/api/weather/${encodeURIComponent(city)}`);
        const data = await response.json();
        
        if (data.success) {
            return data.data;
        } else {
            throw new Error(data.error || 'Failed to fetch weather data');
        }
    } catch (error) {
        console.error('Error fetching weather:', error);
        throw error;
    }
}

// Temperature conversion utilities
function celsiusToFahrenheit(celsius) {
    return (celsius * 9/5) + 32;
}

function fahrenheitToCelsius(fahrenheit) {
    return (fahrenheit - 32) * 5/9;
}

// Format temperature display
function formatTemperature(temp, unit = 'C') {
    return `${Math.round(temp * 10) / 10}°${unit}`;
}

// Get weather icon based on condition
function getWeatherEmoji(condition) {
    const emojiMap = {
        'Clear': '☀️',
        'Clouds': '☁️',
        'Rain': '🌧️',
        'Drizzle': '🌦️',
        'Thunderstorm': '⛈️',
        'Snow': '❄️',
        'Mist': '🌫️',
        'Fog': '🌫️',
        'Haze': '🌫️',
        'Smoke': '💨',
        'Dust': '💨',
        'Sand': '💨',
        'Ash': '🌋',
        'Squall': '💨',
        'Tornado': '🌪️'
    };
    
    return emojiMap[condition] || '🌤️';
}

// Local storage utilities for search history (future enhancement)
function saveSearchHistory(city) {
    try {
        let history = JSON.parse(localStorage.getItem('weatherSearchHistory') || '[]');
        
        // Remove duplicates and add to beginning
        history = history.filter(item => item.toLowerCase() !== city.toLowerCase());
        history.unshift(city);
        
        // Keep only last 10 searches
        history = history.slice(0, 10);
        
        localStorage.setItem('weatherSearchHistory', JSON.stringify(history));
    } catch (error) {
        console.error('Error saving search history:', error);
    }
}

function getSearchHistory() {
    try {
        return JSON.parse(localStorage.getItem('weatherSearchHistory') || '[]');
    } catch (error) {
        console.error('Error getting search history:', error);
        return [];
    }
}

function clearSearchHistory() {
    try {
        localStorage.removeItem('weatherSearchHistory');
    } catch (error) {
        console.error('Error clearing search history:', error);
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Focus search input on '/' key
    if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
        const searchInput = document.querySelector('input[name="city"]');
        if (searchInput && document.activeElement !== searchInput) {
            e.preventDefault();
            searchInput.focus();
        }
    }
    
    // Go to home on 'h' key
    if (e.key === 'h' && e.altKey) {
        e.preventDefault();
        window.location.href = '/';
    }
    
    // Go to about on 'a' key
    if (e.key === 'a' && e.altKey) {
        e.preventDefault();
        window.location.href = '/about';
    }
});

// Add loading state to buttons
function addLoadingState(button) {
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    
    return function removeLoadingState() {
        button.disabled = false;
        button.innerHTML = originalText;
    };
}

// Debounce function for search input
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fetchWeatherAPI,
        celsiusToFahrenheit,
        fahrenheitToCelsius,
        formatTemperature,
        getWeatherEmoji,
        saveSearchHistory,
        getSearchHistory,
        clearSearchHistory,
        showNotification,
        addLoadingState,
        debounce
    };
}

console.log('Weather Info App JavaScript loaded successfully');
