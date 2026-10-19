"use strict";
const form = document.getElementById("calculation");
const result = document.getElementById("result");
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  result.textContent = "Calculating…";
  const payload = {
    price: document.getElementById("price").value,
    rate: document.getElementById("rate").value
  };
  try {
    const response = await fetch("/api/v1/landed-cost", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const value = await response.json();
    if (!response.ok) throw new Error(value.error || "Calculation failed");
    result.textContent = "Total: " + value.total;
  } catch (error) {
    result.textContent = "Error: " + error.message;
  }
});
