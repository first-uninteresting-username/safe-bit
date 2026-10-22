// Functions

function getDisplayedTimestamp() {
  const value = document.getElementById("conversion-result").textContent.trim();
  if (!/^\d+$/.test(value)) {
    return null;
  }

  const timestamp = Number(value);
  return Number.isSafeInteger(timestamp) ? timestamp : null;
}

function getDisplayedSecret() {
  const value = document.getElementById("secret-json-field").textContent;
  let data;
  try {
    data = JSON.parse(value);
  } catch (error) {
    if (error instanceof SyntaxError) {
      return null;
    }
    throw error;
  }

  const secret = data?.["secret-b64"];
  return typeof secret === "string" && secret !== "" ? secret : null;
}

async function generateSecret() {
  const output = document.getElementById("secret-json-field");
  output.hidden = false;
  output.textContent = "Generating secret…";

  try {
    const response = await fetch("/secret");
    if (!response.ok) {
      output.textContent = "Secret generation failed. Please try again.";
      return;
    }

    const data = await response.json();
    output.textContent = JSON.stringify(data, null, 2);
  } catch {
    output.textContent = "Secret generation failed. Please try again.";
  }
}

async function convert_iso(iso_override = null) {
  const iso_input = document.getElementById("iso-datetime");
  const input = document.getElementById("datetime");
  const output = document.getElementById("conversion-result");

  const iso_value = iso_override ?? iso_input.value.trim();
  if (iso_value === "" && input.value === "") {
    output.textContent = "Select a date and time or enter an ISO datetime";
    return null;
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
  return response.ok ? data.timestamp : null;
}

async function generateBit() {
  const input = document.getElementById("bit-request-text");
  const output = document.getElementById("bit-json-field");
  output.hidden = false;
  output.textContent = "Creating bit…";

  let request;
  try {
    request = JSON.parse(input.value);
  } catch (error) {
    if (error instanceof SyntaxError) {
      output.textContent = "Enter valid JSON before creating a bit.";
      return;
    }
    throw error;
  }

  try {
    const response = await fetch("/new-bit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });
    if (!response.ok) {
      output.textContent =
        "Bit creation failed. Check your secret and timestamp and try again.";
      return;
    }

    const data = await response.json();
    output.textContent = JSON.stringify(data, null, 2);
  } catch {
    output.textContent = "Bit creation failed. Please try again.";
  }
}

async function validateBit() {
  const input = document.getElementById("verify-request-text");
  const output = document.getElementById("verify-json-field");
  output.hidden = false;
  output.textContent = "Veryfing bit…";

  let request;
  try {
    request = JSON.parse(input.value);
  } catch (error) {
    if (error instanceof SyntaxError) {
      output.textContent = "Enter valid JSON before validating a bit.";
      return;
    }
    throw error;
  }

  try {
    const response = await fetch("/new-bit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });
    if (!response.ok) {
      output.textContent =
        "Bit validation failed. This most likely means the request is malformed.";
      return;
    }

    const data = await response.json();
    output.textContent = JSON.stringify(data, null, 2);
  } catch {
    output.textContent =
      "Validation failed. Please try again. This most likely means the request is malformed.";
  }
}

function validateJson(field) {
  try {
    JSON.parse(field.value);
    field.setAttribute("aria-invalid", "false");
  } catch {
    field.setAttribute("aria-invalid", "true");
  }
}

// Initial form values

const bitRequestInput = document.getElementById("bit-request-text");
const initialBitRequest = {
  "secret-b64": "",
  timestamp: 12345,
};
bitRequestInput.value = JSON.stringify(initialBitRequest, null, 2);

const verifyRequestInput = document.getElementById("verify-request-text");
const initialVerifyRequest = {
  "secret-b64": "",
  "sha512-secret-b64": null,
  timestamp: 12345,
  commitment: "",
  bit: 0,
};
verifyRequestInput.value = JSON.stringify(initialVerifyRequest, null, 2);

// Datetime converter events

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

// Secret generation events

document
  .getElementById("secret-get-form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();
    await generateSecret();
  });

// Bit creation events

document
  .getElementById("bit-request-form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();
    await generateBit();
  });

document.getElementById("bit-set-secret").addEventListener("click", () => {
  const secret = getDisplayedSecret();
  if (secret === null) {
    alert("Generate a secret first.");
    return;
  }

  const input = document.getElementById("bit-request-text");
  const data = JSON.parse(input.value);
  data["secret-b64"] = secret;
  input.value = JSON.stringify(data, null, 2);
});

document.getElementById("bit-set-date").addEventListener("click", async () => {
  const datepicker = document.getElementById("datetime");
  const date = new Date(datepicker.value);
  if (Number.isNaN(date.getTime())) {
    alert("Select a date and time in the datepicker first.");
    return;
  }

  const timestamp = await convert_iso(date.toISOString());
  if (timestamp === null) {
    return;
  }

  const input = document.getElementById("bit-request-text");
  const data = JSON.parse(input.value);
  data.timestamp = timestamp;
  input.value = JSON.stringify(data, null, 2);
});

// Bit validation events

document
  .getElementById("verify-request-form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();
    await validateBit();
  });

// Validate JSON fields after setting their initial values.

document.querySelectorAll(".json-field").forEach((field) => {
  field.addEventListener("input", () => validateJson(field));
  validateJson(field);
});
