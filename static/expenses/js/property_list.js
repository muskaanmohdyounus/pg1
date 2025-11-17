document.addEventListener("DOMContentLoaded", () => {

    // Input refs
    const searchBar = document.getElementById("searchBar");
    const filterType = document.getElementById("filterType");
    const filterTenant = document.getElementById("filterTenant");
    const clearFilters = document.getElementById("clearFilters");

    // Summary refs
    const sumTotal = document.getElementById("sum_total_properties");
    const sumBeds = document.getElementById("sum_total_beds");
    const sumOccupied = document.getElementById("sum_total_occupied");
    const sumOccPercent = document.getElementById("sum_occupancy_percent");

    // Cards
    const cards = document.querySelectorAll(".property-item");
    const grid = document.getElementById("propertyGrid");

    // MAIN FILTER FUNCTION
    function updateDashboard() {
        const searchVal = searchBar.value.toLowerCase().trim();
        const typeVal = filterType.value;
        const tenantVal = filterTenant.value;

        let visible = 0, totalBeds = 0, occupied = 0;

        cards.forEach(card => {
            const name = card.dataset.name.toLowerCase();
            const city = card.dataset.city.toLowerCase();
            const type = card.dataset.type;
            const tenant = card.dataset.tenant;
            const beds = parseInt(card.dataset.total);
            const occ = parseInt(card.dataset.occ);

            const matchesSearch =
                name.includes(searchVal) ||
                city.includes(searchVal);

            const matchesType =
                typeVal === "" || typeVal === type;

            const matchesTenant =
                tenantVal === "" || tenantVal === tenant;

            const shouldShow =
                matchesSearch && matchesType && matchesTenant;

            if (shouldShow) {
                card.style.display = "block";
                visible++;
                totalBeds += beds;
                occupied += occ;
            } else {
                card.style.display = "none";
            }
        });

        // Update summary card values
        sumTotal.textContent = visible;
        sumBeds.textContent = totalBeds;
        sumOccupied.textContent = occupied;

        const percent = totalBeds > 0 ? Math.round((occupied / totalBeds) * 100) : 0;
        sumOccPercent.textContent = percent + "%";
    }

    // BUTTON EVENTS
    searchBar.addEventListener("input", updateDashboard);
    filterType.addEventListener("change", updateDashboard);
    filterTenant.addEventListener("change", updateDashboard);

    clearFilters.addEventListener("click", () => {
        searchBar.value = "";
        filterType.value = "";
        filterTenant.value = "";
        updateDashboard();
    });

    // INITIAL LOAD
    updateDashboard();
});
