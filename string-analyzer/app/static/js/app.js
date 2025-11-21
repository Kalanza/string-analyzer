// API Base URL
const API_BASE = '/api/v1';

// DOM Elements
const analyzerForm = document.getElementById('analyzerForm');
const stringInput = document.getElementById('stringInput');
const charCount = document.getElementById('charCount');
const resultsCard = document.getElementById('resultsCard');
const closeResults = document.getElementById('closeResults');
const historyGrid = document.getElementById('historyGrid');
const historyLoading = document.getElementById('historyLoading');
const emptyState = document.getElementById('emptyState');
const themeToggle = document.getElementById('themeToggle');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');

// Filter elements
const filterPalindrome = document.getElementById('filterPalindrome');
const minLengthInput = document.getElementById('minLength');
const maxLengthInput = document.getElementById('maxLength');
const wordCountInput = document.getElementById('wordCount');
const applyFiltersBtn = document.getElementById('applyFilters');
const clearFiltersBtn = document.getElementById('clearFilters');
const refreshHistoryBtn = document.getElementById('refreshHistory');

// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const icon = themeToggle.querySelector('i');
    icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
}

// Reveal Animations
function initReveal() {
    const revealItems = document.querySelectorAll('[data-reveal]');
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReduced || !('IntersectionObserver' in window)) {
        revealItems.forEach(item => item.classList.add('is-visible'));
        return () => {};
    }

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = entry.target.dataset.revealDelay || 0;
                entry.target.style.transitionDelay = `${delay}ms`;
                entry.target.classList.add('is-visible');
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.25, rootMargin: '0px 0px -60px 0px' });

    revealItems.forEach(item => observer.observe(item));

    return () => observer.disconnect();
}

// Toast Notification
function showToast(message, type = 'success') {
    toastMessage.textContent = message;
    const icon = toast.querySelector('i');
    
    if (type === 'success') {
        icon.className = 'fas fa-check-circle';
        icon.style.color = 'var(--success)';
    } else if (type === 'error') {
        icon.className = 'fas fa-exclamation-circle';
        icon.style.color = 'var(--danger)';
    }
    
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Character Counter
stringInput.addEventListener('input', (e) => {
    charCount.textContent = e.target.value.length;
});

// Analyze String
analyzerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const value = stringInput.value.trim();
    if (!value) {
        showToast('Please enter some text to analyze', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/strings/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ value })
        });
        
        if (!response.ok) {
            throw new Error('Failed to analyze string');
        }
        
        const data = await response.json();
        displayResults(data);
        showToast('String analyzed successfully!');
        
        // Refresh history after a short delay
        setTimeout(() => loadHistory(), 500);
        
    } catch (error) {
        console.error('Error:', error);
        showToast('Failed to analyze string. Please try again.', 'error');
    }
});

// Display Results
function displayResults(data) {
    // Show results card
    resultsCard.style.display = 'block';
    resultsCard.classList.add('is-visible');
    
    // Palindrome status
    const palindromeResult = document.getElementById('palindromeResult');
    const palindromeValue = document.getElementById('palindromeValue');
    
    if (data.is_palindrome) {
        palindromeResult.classList.add('is-palindrome');
        palindromeResult.classList.remove('not-palindrome');
        palindromeValue.innerHTML = '<i class="fas fa-check-circle"></i> Yes, it\'s a palindrome!';
        palindromeValue.style.color = 'var(--success)';
    } else {
        palindromeResult.classList.add('not-palindrome');
        palindromeResult.classList.remove('is-palindrome');
        palindromeValue.innerHTML = '<i class="fas fa-times-circle"></i> Not a palindrome';
        palindromeValue.style.color = 'var(--text-secondary)';
    }
    
    // Other values
    document.getElementById('lengthValue').textContent = data.length;
    document.getElementById('wordCountValue').textContent = data.word_count;
    document.getElementById('uniqueCharsValue').textContent = data.unique_characters;
    document.getElementById('hashValue').textContent = data.sha256_hash;
    
    // Character frequency
    displayFrequency(data.character_frequency_map);
    
    // Scroll to results
    resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Display Character Frequency
function displayFrequency(freqMap) {
    const chart = document.getElementById('frequencyChart');
    chart.innerHTML = '';
    
    // Sort by frequency (highest first)
    const sorted = Object.entries(freqMap).sort((a, b) => b[1] - a[1]);
    const maxFreq = sorted[0] ? sorted[0][1] : 1;
    
    sorted.forEach(([char, count]) => {
        const percentage = (count / maxFreq) * 100;
        
        const barHtml = `
            <div class="freq-bar">
                <span class="freq-char">'${char}'</span>
                <div class="freq-bar-container">
                    <div class="freq-bar-fill" style="width: ${percentage}%">
                        ${count}
                    </div>
                </div>
            </div>
        `;
        
        chart.innerHTML += barHtml;
    });
}

// Close Results
closeResults.addEventListener('click', () => {
    resultsCard.style.display = 'none';
});

// Load History
async function loadHistory(filters = {}) {
    historyLoading.style.display = 'block';
    emptyState.style.display = 'none';
    historyGrid.innerHTML = '<div class="loading" id="historyLoading"><i class="fas fa-spinner fa-spin"></i> Loading history...</div>';
    
    try {
        // Build query params
        const params = new URLSearchParams();
        if (filters.is_palindrome !== undefined) {
            params.append('is_palindrome', filters.is_palindrome);
        }
        if (filters.min_length) {
            params.append('min_length', filters.min_length);
        }
        if (filters.max_length) {
            params.append('max_length', filters.max_length);
        }
        if (filters.word_count) {
            params.append('word_count', filters.word_count);
        }
        
        const url = `${API_BASE}/strings/${params.toString() ? '?' + params.toString() : ''}`;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error('Failed to load history');
        }
        
        const data = await response.json();
        displayHistory(data.results);
        updateStats(data.results);
        
    } catch (error) {
        console.error('Error:', error);
        historyGrid.innerHTML = `
            <div class="loading">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Failed to load history</p>
            </div>
        `;
    }
}

// Display History
function displayHistory(items) {
    historyGrid.innerHTML = '';
    
    if (items.length === 0) {
        emptyState.style.display = 'block';
        return;
    }
    
    items.forEach(item => {
        const date = new Date(item.created_at).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.innerHTML = `
            <div class="history-value">${escapeHtml(item.value)}</div>
            <div class="history-badges">
                ${item.is_palindrome ? '<span class="badge badge-success"><i class="fas fa-check"></i> Palindrome</span>' : ''}
                <span class="badge badge-info">${item.length} chars</span>
                <span class="badge badge-info">${item.word_count} words</span>
                <span class="badge badge-info">${item.unique_characters} unique</span>
            </div>
            <div class="history-meta">
                <span><i class="fas fa-clock"></i> ${date}</span>
                <button class="delete-btn" onclick="deleteString('${escapeHtml(item.value)}')">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        
        historyGrid.appendChild(historyItem);
    });
}

// Update Stats
function updateStats(items) {
    const totalAnalyzed = items.length;
    const palindromeCount = items.filter(item => item.is_palindrome).length;
    
    document.getElementById('totalAnalyzed').textContent = totalAnalyzed;
    document.getElementById('palindromeCount').textContent = palindromeCount;
}

// Delete String
async function deleteString(value) {
    if (!confirm(`Are you sure you want to delete "${value}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/strings/${encodeURIComponent(value)}`, {
            method: 'DELETE'
        });
        
        if (response.status === 204) {
            showToast('String deleted successfully!');
            loadHistory();
        } else {
            throw new Error('Failed to delete string');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showToast('Failed to delete string. Please try again.', 'error');
    }
}

// Apply Filters
applyFiltersBtn.addEventListener('click', () => {
    const filters = {};
    
    if (filterPalindrome.checked) {
        filters.is_palindrome = true;
    }
    
    if (minLengthInput.value) {
        filters.min_length = parseInt(minLengthInput.value);
    }
    
    if (maxLengthInput.value) {
        filters.max_length = parseInt(maxLengthInput.value);
    }
    
    if (wordCountInput.value) {
        filters.word_count = parseInt(wordCountInput.value);
    }
    
    loadHistory(filters);
    showToast('Filters applied');
});

// Clear Filters
clearFiltersBtn.addEventListener('click', () => {
    filterPalindrome.checked = false;
    minLengthInput.value = '';
    maxLengthInput.value = '';
    wordCountInput.value = '';
    
    loadHistory();
    showToast('Filters cleared');
});

// Refresh History
refreshHistoryBtn.addEventListener('click', () => {
    loadHistory();
    showToast('History refreshed');
});

// Utility: Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Smooth Scrolling for Navigation Links
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        if (link.getAttribute('href').startsWith('#')) {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
                
                // Update active link
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            }
        }
    });
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initReveal();
    document.body.classList.remove('no-motion');
    loadHistory();
    
    // Theme toggle event
    themeToggle.addEventListener('click', toggleTheme);
});
