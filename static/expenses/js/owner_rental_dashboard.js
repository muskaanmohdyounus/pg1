// -------------------------------------------------------------
// OWNER RENTAL DASHBOARD – SPA FRONTEND JS
// -------------------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {

    const searchInput = document.getElementById("searchInput");
    const rows = document.querySelectorAll("#rentalTable tbody tr");
    const tabs = document.querySelectorAll(".rental-tab");

    // ---------------------------------------------------------
    // TAB FILTERING
    // ---------------------------------------------------------
    tabs.forEach(tab => {
        tab.addEventListener("click", () => {

            // remove active from all
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");

            const tabType = tab.dataset.type; // upcoming, pending, paid, all

            rows.forEach(row => {
                const status = row.dataset.status; // upcoming/pending/paid

                if (tabType === "all" || tabType === status) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
            });
        });
    });

    // ---------------------------------------------------------
    // SEARCH FILTERING
    // ---------------------------------------------------------
    if (searchInput) {
        searchInput.addEventListener("keyup", () => {
            const value = searchInput.value.toLowerCase().trim();

            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(value) ? "" : "none";
            });
        });
    }

});
