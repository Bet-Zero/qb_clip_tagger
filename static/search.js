function populateSearch() {
  const params = new URLSearchParams(window.location.search);

  // Find the matching playtype option by its value
  const playSelect = document.querySelector("select[name='playtype']");
  if (playSelect) {
    const playValue = params.get("playtype");
    const playOption = Array.from(playSelect.options).find(
      (opt) => opt.value === playValue
    );
    if (playOption) playSelect.value = playValue;
  }

  // Find the matching situation option by its value
  const situationSelect = document.querySelector("select[name='situation']");
  if (situationSelect) {
    const situationValue = params.get("situation");
    const situationOption = Array.from(situationSelect.options).find(
      (opt) => opt.value === situationValue
    );
    if (situationOption) situationSelect.value = situationValue;
  }

  // Simple selects that use same value for both option text and value
  const outcomeSelect = document.querySelector("select[name='outcome']");
  if (outcomeSelect) outcomeSelect.value = params.get("outcome") || "";

  const contextSelect = document.querySelector("select[name='context']");
  if (contextSelect) contextSelect.value = params.get("context") || "";

  const qualityVal = params.get("quality");
  if (qualityVal) {
    document
      .querySelectorAll(".quality-group .toggle-button")
      .forEach((btn) => {
        btn.classList.toggle("selected", btn.dataset.value === qualityVal);
      });
    const hidden = document.querySelector('input[name="quality"]');
    if (hidden) hidden.value = qualityVal;
  }

  // Role handling - set select and hidden input
  const rolesVal = params.get("roles");
  if (rolesVal) {
    const roleSelect = document.querySelector("select[name='role']");
    if (roleSelect) roleSelect.value = rolesVal;
    if (typeof updateRoles === "function") updateRoles();
  }

  function setTagSelections(field) {
    const val = params.get(field);
    if (!val) return;
    const selections = val.split(",").filter(Boolean);
    document
      .querySelectorAll(
        `.selectable[data-field='${field}'], .chip[data-field='${field}']`
      )
      .forEach((el) => {
        el.classList.toggle("selected", selections.includes(el.textContent));
      });
    const input = document.querySelector(`input[name='${field}']`);
    if (input) input.value = val;
  }

  ["traits", "badges", "subroles"].forEach(setTagSelections);
}

// populateTags is already called by taggerData.js, just run populateSearch
window.addEventListener("DOMContentLoaded", () => {
  // Add click handlers for traits and badges chips after they're created
  setTimeout(() => {
    document
      .querySelectorAll(
        '.chip-row[data-field="traits"] .chip, .chip-row[data-field="badges"] .chip'
      )
      .forEach((chip) => {
        chip.addEventListener("click", toggleSelectLabel);
      });
  }, 0); // Run after current execution context
  
  populateSearch();
});

function showInFinder(path) {
  fetch("/reveal", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path }),
  }).catch((err) => console.error("Failed to reveal", err));
}

function showListInFinder() {
  const paths = [...document.querySelectorAll("#results-list li")].map(
    (li) => li.dataset.path
  );
  fetch("/reveal_list", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ paths }),
  }).catch((err) => console.error("Failed to reveal list", err));
}
