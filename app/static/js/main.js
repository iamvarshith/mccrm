// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});

// Dynamic policy form handling
function updatePolicyFields() {
    const policyType = document.getElementById('policy_type');
    const globalPolicySelect = document.getElementById('global_policy_id');
    const customPolicySelect = document.getElementById('custom_policy_id');
    
    if (policyType) {
        if (policyType.value === 'global') {
            globalPolicySelect.style.display = 'block';
            customPolicySelect.style.display = 'none';
        } else {
            globalPolicySelect.style.display = 'none';
            customPolicySelect.style.display = 'block';
        }
    }
}

// Premium calculation
function calculatePremium() {
    const baseAmount = parseFloat(document.getElementById('base_amount').value) || 0;
    const duration = parseInt(document.getElementById('duration_months').value) || 0;
    const dependents = document.querySelectorAll('input[name="dependents"]:checked').length;
    
    let premium = baseAmount;
    
    // Add 10% for each dependent
    if (dependents > 0) {
        premium += (premium * (dependents * 0.1));
    }
    
    // Apply duration discount
    if (duration >= 12) {
        premium *= 0.95; // 5% discount for annual policies
    }
    
    document.getElementById('premium_amount').value = premium.toFixed(2);
}

// Search functionality
function handleSearch(event) {
    const searchForm = event.target.closest('form');
    const searchInput = searchForm.querySelector('input[name="search"]');
    
    if (searchInput.value.length < 2 && searchInput.value.length > 0) {
        event.preventDefault();
        alert('Please enter at least 2 characters to search');
    }
}

// Date validation
function validateDates() {
    const startDate = document.getElementById('start_date');
    const today = new Date().toISOString().split('T')[0];
    startDate.min = today;
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Handle dependent selection
function handleDependentSelection() {
    const groupPolicy = document.getElementById('is_group_policy');
    const dependentsSection = document.getElementById('dependents_section');
    
    if (groupPolicy) {
        dependentsSection.style.display = groupPolicy.checked ? 'block' : 'none';
    }
}

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Policy type change
    const policyTypeSelect = document.getElementById('policy_type');
    if (policyTypeSelect) {
        policyTypeSelect.addEventListener('change', updatePolicyFields);
    }
    
    // Premium calculation
    const premiumInputs = document.querySelectorAll('.premium-input');
    premiumInputs.forEach(input => {
        input.addEventListener('change', calculatePremium);
    });
    
    // Search forms
    const searchForms = document.querySelectorAll('.search-form');
    searchForms.forEach(form => {
        form.addEventListener('submit', handleSearch);
    });
    
    // Date inputs
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        validateDates();
    });
    
    // Group policy checkbox
    const groupPolicyCheckbox = document.getElementById('is_group_policy');
    if (groupPolicyCheckbox) {
        groupPolicyCheckbox.addEventListener('change', handleDependentSelection);
    }
}); 