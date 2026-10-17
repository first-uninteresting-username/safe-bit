async function convert_iso() {
  const input = document.getElementById("date-time");
  const output = document.getElementById("conversion-result");

  const response = await fetch("/time-for-iso", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      iso: input.value,
    }),
  });

  const data = await response.json();
  output.textContent = response.ok ? data.timestamp : "Conversion failed";
}

document
  .getElementById("converter-form")
  .addEventListener("submit", (event) => {
    event.preventDefault();
    convert_iso();
  });

document.getElementById("now-button").addEventListener("click", () => {
  const input = document.getElementById("date-time");
  input.value = new Date().toISOString();
});

const datepicker = document.getElementById("datepicker");
const toggleDatepicker = document.getElementById("toggle-datepicker");

toggleDatepicker.addEventListener("click", () => {
  datepicker.hidden = !datepicker.hidden;
  toggleDatepicker.textContent = datepicker.hidden
    ? "Open datepicker"
    : "Close datepicker";
  toggleDatepicker.setAttribute("aria-expanded", String(!datepicker.hidden));
});

document
  .getElementById("copy-button-converter")
  .addEventListener("click", async () => {
    const input = document.getElementById("conversion-result");
    await navigator.clipboard.writeText(input.textContent);
  });
