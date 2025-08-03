document.addEventListener("DOMContentLoaded", async function() {
    const select = document.getElementById("company-select");
    const tbody = document.getElementById("stock-data");

    async function fetchData(ticker) {
        try {
            const response = await fetch(`/api/stock/${ticker}`);
            const data = await response.json();
            tbody.innerHTML = '';

            data.results.forEach(result => {
                const row = document.createElement("tr");

                const date = new Date(result.t);
                const dateString = date.toLocaleDateString();

                row.innerHTML = `
                    <td>${dateString}</td>
                    <td>${result.v}</td>
                    <td>${result.vw.toFixed(2)}</td>
                    <td>${result.o.toFixed(2)}</td>
                    <td>${result.c.toFixed(2)}</td>
                    <td>${result.h.toFixed(2)}</td>
                    <td>${result.l.toFixed(2)}</td>
                    <td>${result.n}</td>
                `;

                tbody.appendChild(row);
            });
        } catch (e) {
            console.error('An error occurred while fetching data:', e);
        }
    }

    select.addEventListener("change", function() {
        fetchData(select.value);
    });

    fetchData(select.value); // Fetch data for the default selected company on page load
});
