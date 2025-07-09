function populateSearch() {
  const playSelect = document.querySelector("select[name='playtype']");
  const situationSelect = document.querySelector("select[name='situation']");
  const outcomeSelect = document.querySelector("select[name='outcome']");
  const contextSelect = document.querySelector("select[name='context']");

  if (playSelect) {
    const playPlaceholder = new Option("Play Type", "");
    playPlaceholder.className = "placeholder-option";
    playSelect.add(playPlaceholder);
    if (window.playTypes) {
      window.playTypes.forEach((p) => playSelect.add(new Option(p, p)));
    }
    playSelect.value =
      new URLSearchParams(window.location.search).get("playtype") || "";
  }

  if (situationSelect) {
    const sitPlaceholder = new Option("Situation", "");
    sitPlaceholder.className = "placeholder-option";
    situationSelect.add(sitPlaceholder);
    if (window.situations) {
      window.situations.forEach((s) => situationSelect.add(new Option(s, s)));
    }
    situationSelect.value =
      new URLSearchParams(window.location.search).get("situation") || "";
  }

  if (outcomeSelect) {
    const outPlaceholder = new Option("Outcome", "");
    outPlaceholder.className = "placeholder-option";
    outcomeSelect.add(outPlaceholder);
    if (window.outcomes) {
      window.outcomes.forEach((o) => outcomeSelect.add(new Option(o, o)));
    }
    outcomeSelect.value =
      new URLSearchParams(window.location.search).get("outcome") || "";
  }

  if (contextSelect) {
    const ctxPlaceholder = new Option("Context", "");
    ctxPlaceholder.className = "placeholder-option";
    contextSelect.add(ctxPlaceholder);
    if (window.contexts) {
      window.contexts.forEach((c) => contextSelect.add(new Option(c, c)));
    }
    contextSelect.value =
      new URLSearchParams(window.location.search).get("context") || "";
  }
}

window.addEventListener("DOMContentLoaded", populateSearch);
