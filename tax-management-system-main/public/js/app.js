document.getElementById('taxForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    // UI Element Selectors
    const financialYear = document.getElementById('financialYear').value;
    const grossIncomeInput = document.getElementById('grossIncome');
    const deductionsInput = document.getElementById('deductions');
    const grossError = document.getElementById('grossError');
    const deductionsError = document.getElementById('deductionsError');
    
    const placeholderText = document.getElementById('placeholderText');
    const resultDisplay = document.getElementById('resultDisplay');
    const resTaxableIncome = document.getElementById('resTaxableIncome');
    const resTaxPayable = document.getElementById('resTaxPayable');

    // Values Conversion
    const grossIncome = parseFloat(grossIncomeInput.value) || 0;
    const deductions = parseFloat(deductionsInput.value) || 0;

    // Fast-fail Client-side Validation Checks
    let isValid = true;
    grossError.style.display = 'none';
    deductionsError.style.display = 'none';

    if (grossIncome <= 0) {
        grossError.style.display = 'block';
        isValid = false;
    }
    if (deductions > grossIncome) {
        deductionsError.style.display = 'block';
        isValid = false;
    }

    if (!isValid) return;

    // Construct the data payload matching our backend expectations
    const payload = {
        financial_year: financialYear,
        gross_income: grossIncome,
        deductions: deductions
    };

    try {
        // Dispatch asynchronous POST network request to the Flask Server
        const response = await fetch('/api/calculate-tax', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.error || 'Server rejected calculation parameters.');
            return;
        }

        // Dynamically map backend calculated data structures back onto the view layout
        resTaxableIncome.textContent = `₹${result.taxable_income.toLocaleString('en-IN')}`;
        resTaxPayable.textContent = `₹${result.tax_payable.toLocaleString('en-IN')}`;

        // Modify UI panel presentation state
        placeholderText.classList.add('hidden');
        resultDisplay.classList.remove('hidden');

        refreshCalculationLog();

    } catch (error) {
        console.error('API Communication Failure:', error);
        alert('Could not establish contact with the calculation server backend.');
    }
});

// Function to fetch log records from backend API and render them inside the HTML DOM
async function refreshCalculationLog() {
    const tableBody = document.getElementById('logTableBody');
    if (!tableBody) return;

    try {
        const response = await fetch('/api/tax-records');
        const records = await response.json();

        if (!response.ok) throw new Error('Data fetch rejected by api');

        // Clear existing static rows inside the body container
        tableBody.innerHTML = '';

        if (records.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="6" style="text-align:center; color: var(--text-muted);">No tax calculation history records found in database.</td></tr>`;
            return;
        }

        // Generate structural data elements dynamically 
        records.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>#${row.record_id}</strong></td>
                <td>${row.email}</td>
                <td>${row.financial_year}</td>
                <td>₹${row.gross_income.toLocaleString('en-IN')}</td>
                <td>₹${row.deductions.toLocaleString('en-IN')}</td>
                <td><span style="color: var(--success-text); font-weight:600;">₹${row.tax_payable.toLocaleString('en-IN')}</span></td>
            `;
            tableBody.appendChild(tr);
        });

    } catch (err) {
        console.error('Error rendering log panel visual properties:', err);
    }
}

// Hook up listener actions to the manual refresh button asset element
document.getElementById('refreshLogBtn').addEventListener('click', refreshCalculationLog);

// Trigger a structural view data download instantly as soon as the front-end loads up in browser
document.addEventListener('DOMContentLoaded', refreshCalculationLog);