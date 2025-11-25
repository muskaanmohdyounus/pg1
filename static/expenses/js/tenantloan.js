document.addEventListener('DOMContentLoaded', function() {
  const openFilter = document.getElementById('openFilter');
  const closeFilter = document.getElementById('closeFilter');
const filterSidebar = document.querySelector('.filter-sidebar');


  if (openFilter) openFilter.addEventListener('click', () => filterSidebar.classList.add('active'));
  if (closeFilter) closeFilter.addEventListener('click', () => filterSidebar.classList.remove('active'));

  // Optional: Calculate monthly installment live when repay months or amount fields change (on apply/edit forms)
  const amountInput = document.querySelector('input[name="loan_amount_requested"]');
  const monthsInput = document.querySelector('input[name="repayment_months"]');
  if (amountInput && monthsInput) {
    const compute = () => {
      const amount = parseFloat(amountInput.value) || 0;
      const months = parseInt(monthsInput.value) || 1;
      const emi = (months > 0) ? (amount / months).toFixed(2) : '0.00';
      // Optionally show EMI to user
      let emiElem = document.getElementById('live-emi');
      if (!emiElem) {
        emiElem = document.createElement('div');
        emiElem.id = 'live-emi';
        amountInput.parentNode.appendChild(emiElem);
      }
      emiElem.textContent = `Estimated monthly installment: ₹${emi}`;
    };
    amountInput.addEventListener('input', compute);
    monthsInput.addEventListener('input', compute);
    compute();
  }
});
