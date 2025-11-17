document.addEventListener('DOMContentLoaded', () => {

    // ---------------------------
    // 1. Clickable table rows -> expense detail page
    // ---------------------------
  document.querySelectorAll('.clickable-row').forEach(row => {
    row.addEventListener('click', (e) => {
        // Ignore clicks on links inside the row
        if (e.target.tagName.toLowerCase() === 'a') return;

        const url = row.dataset.url;  // use the full URL from the template
        if (url) window.location.href = url;
    });
});

 // ---------------------------
// 2. Category Doughnut Chart
// ---------------------------
const labels = JSON.parse(document.getElementById('chart-labels').textContent);
const data = JSON.parse(document.getElementById('chart-values').textContent);


const ctx = document.getElementById('categoryChart').getContext('2d');
const colors = ['#f87171','#ef4444','#b91c1c','#fecaca','#fb7185','#fca5a5','#fbbf24','#facc15'];

const categoryChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: labels,
        datasets: [{
            data: data,
            backgroundColor: colors,
            borderColor: '#ffffff',
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    boxWidth: 20,
                    padding: 15
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return `${context.label}: ₹${context.raw}`;
                    }
                }
            }
        }
    }
});

    // ---------------------------
    // 3. Read More Toggle (if needed)
    // ---------------------------
    document.querySelectorAll(".read-more-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const cell = btn.parentElement;
            const shortText = cell.querySelector(".short-text");
            const fullText = cell.querySelector(".full-text");

            if (fullText.style.display === "none") {
                fullText.style.display = "inline";
                shortText.style.display = "none";
                btn.textContent = "Read less";
            } else {
                fullText.style.display = "none";
                shortText.style.display = "inline";
                btn.textContent = "Read more";
            }
        });
    });

    // ---------------------------
    // 4. Filter Reset Button
    // ---------------------------
 // Open & Close Sidebar
const sidebar = document.getElementById("filterSidebar");
document.getElementById("openFilter").addEventListener("click", () => sidebar.classList.add("active"));
document.getElementById("closeFilter").addEventListener("click", () => sidebar.classList.remove("active"));

// Quick Date Buttons
document.querySelectorAll(".quick-date").forEach(btn => {
    btn.addEventListener("click", () => {
        const days = parseInt(btn.dataset.range);
        const endDate = new Date();
        const startDate = new Date();
        startDate.setDate(endDate.getDate() - days + 1);

        document.getElementById("startDate").value = startDate.toISOString().split('T')[0];
        document.getElementById("endDate").value = endDate.toISOString().split('T')[0];
    });
});

// Apply Filters
document.getElementById("applyFilters").addEventListener("click", () => {
    const filters = {
        title: document.getElementById("title").value,
        category: document.getElementById("category").value,
        property: document.getElementById("property").value,
        minAmount: document.getElementById("minAmount").value,
        maxAmount: document.getElementById("maxAmount").value,
        startDate: document.getElementById("startDate").value,
        endDate: document.getElementById("endDate").value,
        hasBill: document.getElementById("hasBill").checked
    };
    console.log("Filters Applied:", filters);
    sidebar.classList.remove("active");
});

// Reset Filters
document.getElementById("resetFilters").addEventListener("click", () => {
    document.querySelectorAll("#filterSidebar input, #filterSidebar select").forEach(el => {
        if(el.type === "checkbox") el.checked = false;
        else el.value = "";
    });
});


    // ---------------------------
    // 5. Optional: Dynamic Chart Update (on filters change)
    // ---------------------------
    const filterInputs = document.querySelectorAll('#searchCategory, input[name="start_date"], input[name="end_date"]');
    filterInputs.forEach(input => {
        input.addEventListener('change', () => {
            // Here you can add AJAX/fetch request to get filtered categoryData
            // and update the chart dynamically:
            // categoryChart.data.labels = newLabels;
            // categoryChart.data.datasets[0].data = newData;
            // categoryChart.update();
        });
    });
});
