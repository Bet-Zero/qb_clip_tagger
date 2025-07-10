// Enable scrollable suggestions for player input fields
function enablePlayerSuggestions(input, players) {
  if (!input) return;
  const wrapper = input.parentElement;
  if (!wrapper) return;
  wrapper.style.position = wrapper.style.position || "relative";

  const box = document.createElement("div");
  box.className = "player-suggestions";
  box.style.display = "none";
  wrapper.appendChild(box);

  function renderList(value) {
    const query = value.toLowerCase();
    box.innerHTML = "";
    players
      .filter((p) => p.toLowerCase().includes(query))
      .slice(0, 50)
      .forEach((p) => {
        const item = document.createElement("div");
        item.textContent = p;
        item.addEventListener("mousedown", (e) => {
          e.preventDefault();
          input.value = p;
          box.style.display = "none";
        });
        box.appendChild(item);
      });
    box.style.display = box.childElementCount ? "block" : "none";
  }

  input.addEventListener("input", () => renderList(input.value));
  input.addEventListener("focus", () => renderList(input.value));
  input.addEventListener("blur", () =>
    setTimeout(() => (box.style.display = "none"), 100)
  );
}
