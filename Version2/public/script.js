document.addEventListener("DOMContentLoaded", async function () {
  const select = document.getElementById("company-select");
  const tbody = document.getElementById("stock-data");

  async function fetchData(ticker) {
    try {
      const response = await fetch(`/api/stock?ticker=${ticker}`);
      const data = await response.json();
      tbody.innerHTML = "";

      if (!data.results) {
        tbody.innerHTML = "<tr><td colspan='8'>No data available</td></tr>";
        return;
      }

      data.results.forEach(result => {
        const date = new Date(result.t);
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${date.toLocaleDateString()}</td>
          <td>${result.v}</td>
          <td>${result.vw?.toFixed(2) || "-"}</td>
          <td>${result.o?.toFixed(2) || "-"}</td>
          <td>${result.c?.toFixed(2) || "-"}</td>
          <td>${result.h?.toFixed(2) || "-"}</td>
          <td>${result.l?.toFixed(2) || "-"}</td>
          <td>${result.n}</td>
        `;
        tbody.appendChild(row);
      });
    } catch (e) {
      console.error("Error fetching data:", e);
      tbody.innerHTML = "<tr><td colspan='8'>Error loading data</td></tr>";
    }
  }

  select.addEventListener("change", () => fetchData(select.value));
  fetchData(select.value);
});
