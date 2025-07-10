function populateSearch() {
  const params = new URLSearchParams(window.location.search);

  const playSelect = document.querySelector("select[name='playtype']");
  if (playSelect) playSelect.value = params.get("playtype") || "";

  const situationSelect = document.querySelector("select[name='situation']");
  if (situationSelect) situationSelect.value = params.get("situation") || "";

  const outcomeSelect = document.querySelector("select[name='outcome']");
  if (outcomeSelect) outcomeSelect.value = params.get("outcome") || "";

  const contextSelect = document.querySelector("select[name='context']");
  if (contextSelect) contextSelect.value = params.get("context") || "";

  // Roles (offense/defense selects)
  const rolesVal = params.get("roles");
  if (rolesVal) {
    const [off, def] = rolesVal.split(",");
    const offenseSelect = document.querySelector("select[name='offense_role']");
    const defenseSelect = document.querySelector("select[name='defense_role']");
    if (offenseSelect) offenseSelect.value = off || "";
    if (defenseSelect) defenseSelect.value = def || "";
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
        if (selections.includes(el.textContent)) {
          el.classList.add("selected");
        }
      });
    const input = document.querySelector(`input[name='${field}']`);
    if (input) input.value = val;
  }

  ["traits", "badges", "subroles"].forEach(setTagSelections);
}

window.addEventListener("DOMContentLoaded", populateSearch);

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
