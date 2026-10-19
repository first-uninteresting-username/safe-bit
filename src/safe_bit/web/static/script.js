async function convert_iso() {
  const iso_input = document.getElementById("iso-datetime");
  const input = document.getElementById("datetime");
  const output = document.getElementById("conversion-result");

  const iso_value = iso_input.value.trim();
  if (iso_value === "" && input.value === "") {
    output.textContent = "Select a date and time or enter an ISO datetime";
    return;
  }

  const field =
    iso_value === "" ? new Date(input.value).toISOString() : iso_value;

  const response = await fetch("/time-for-iso", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      iso: field,
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
  const field = document.getElementById("datetime");
  const iso_field = document.getElementById("iso-datetime");
  const now = new Date();
  const pad = (number) => String(number).padStart(2, "0");

  iso_field.value = now.toISOString();
  field.value =
    `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}` +
    `T${pad(now.getHours())}:${pad(now.getMinutes())}`;
});

const iso_datepicker = document.getElementById("iso-datepicker");
const toggleDatepicker = document.getElementById("toggle-datepicker");

toggleDatepicker.addEventListener("click", () => {
  iso_datepicker.hidden = !iso_datepicker.hidden;
  toggleDatepicker.textContent = iso_datepicker.hidden
    ? "Open datepicker"
    : "Close datepicker";
  toggleDatepicker.setAttribute(
    "aria-expanded",
    String(!iso_datepicker.hidden),
  );
});

document
  .getElementById("copy-button-converter")
  .addEventListener("click", async () => {
    const input = document.getElementById("conversion-result");
    await navigator.clipboard.writeText(input.textContent);
  });

document
  .getElementById("secret-get-form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();
    const output = document.getElementById("secret-json-field");

    try {
      const response = await fetch("/secret");
      if (!response.ok) {
        throw new Error("Secret request failed");
      }
      const data = await response.json();
      output.textContent = JSON.stringify(data, null, 2);
    } catch {
      output.textContent = "Could not fetch secret. Please try again.";
    }
    output.hidden = false;
  });

function validateJson(field) {
  try {
    JSON.parse(field.value);
    field.setAttribute("aria-invalid", "false");
  } catch {
    field.setAttribute("aria-invalid", "true");
  }
}

document.querySelectorAll(".json-field").forEach((field) => {
  field.addEventListener("input", () => validateJson(field));
  validateJson(field);
});
