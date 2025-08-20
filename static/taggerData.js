const offensiveRoles = [
  "Pocket Passer",
  "Dual-Threat QB",
  "Mobile QB",
  "Game Manager",
  "Gunslinger",
  "Field General",
  "Read-Option QB",
  "RPO Specialist",
  "Scrambler",
  "Red Zone Specialist",
];

const offensiveSubrolesPositive = [
  "Accurate Passer",
  "Deep Ball Thrower",
  "Quick Release",
  "Pocket Presence",
  "Mobility",
  "Field Vision",
  "Pre-Snap Read",
  "Post-Snap Read",
  "Pressure Handler",
  "Red Zone Efficiency",
  "Third Down Converter",
  "Clutch Performer",
  "Touchdown Creator",
  "Big Play Maker",
];

const offensiveSubrolesNegative = [
  "Inaccurate Passes",
  "Poor Decision Making",
  "Slow Release",
  "Pressure Sensitivity",
  "Limited Mobility",
  "Poor Field Vision",
  "Misses Reads",
  "Interception Prone",
  "Fumble Issues",
  "Red Zone Struggles",
  "Third Down Failures",
  "Clock Management",
  "Overthrows",
  "Poor Timing",
  "Stares Down Receivers",
];


const traits = [
  "Arm Strength",
  "Accuracy",
  "Mobility",
  "Decision Making",
  "Field Vision",
  "Leadership",
  "Pocket Presence",
  "Football IQ",
  "Clutch",
];

const badges = [
  "Cannon Arm",
  "Surgeon",
  "Scrambler",
  "Field General",
  "Gunslinger",
  "Pocket Passer",
  "Dual Threat",
  "Game Manager",
  "Clutch",
  "High Motor",
  "High IQ",
  "Coach's Dream",
  "Versatile",
  "Chess Piece",
  "Dawg",
  "Leader",
  "Franchise QB",
  "Game Changer",
  "Playmaker",
  "Ice in Veins",
  "Iron Man",
  "Cool Under Pressure",
  "Veteran Presence",
];

const playTypes = [
  { label: "Drop Back Pass", value: "dropback-pass" },
  { label: "Quick Slant", value: "quick-slant" },
  { label: "Deep Ball", value: "deep-ball" },
  { label: "Checkdown", value: "checkdown" },
  { label: "Screen Pass", value: "screen-pass" },
  { label: "Roll Out", value: "rollout" },
  { label: "Play Action", value: "play-action" },
  { label: "RPO", value: "rpo" },
  { label: "Read Option", value: "read-option" },
  { label: "Scramble", value: "scramble" },
  { label: "Designed Run", value: "designed-run" },
  { label: "Bootleg", value: "bootleg" },
  { label: "Pocket Movement", value: "pocket-movement" },
  { label: "Hot Route", value: "hot-route" },
  { label: "Audible", value: "audible" },
  { label: "Two Minute Drill", value: "two-minute" },
  { label: "Red Zone", value: "red-zone" },
  { label: "Goal Line", value: "goal-line" },
  { label: "Hail Mary", value: "hail-mary" },
];

const outcomes = [
  "Completion",
  "Incompletion", 
  "Touchdown",
  "Interception",
  "Fumble",
  "Sack",
  "Scramble",
  "Throwaway",
  "Penalty",
  "First Down",
  "Turnover on Downs",
  "Safety",
];

const situations = [
  { label: "Clean Pocket", value: "clean-pocket" },
  { label: "Pressure", value: "pressure" },
  { label: "Blitz", value: "blitz" },
  { label: "Red Zone", value: "red-zone" },
  { label: "Goal Line", value: "goal-line" },
  { label: "Third Down", value: "third-down" },
  { label: "Fourth Down", value: "fourth-down" },
  { label: "Two Minute Warning", value: "two-minute" },
  { label: "Overtime", value: "overtime" },
  { label: "Hurry Up", value: "hurry-up" },
];

const contexts = ["1Q", "2Q", "3Q", "4Q", "OT"];

function toggleSelectLabel(event) {
  const target = event.currentTarget || event.target;
  target.classList.toggle("selected");
  const field = target.dataset.field;
  const input = document.querySelector(`input[name="${field}"]`);
  const selected = [
    ...document.querySelectorAll(
      `.selectable[data-field="${field}"].selected, .chip[data-field="${field}"].selected`
    ),
  ].map((el) => el.textContent);
  if (input) input.value = selected.join(",");
  if (field === "subroles") {
    localStorage.setItem("lastSubroles", input.value);
  }
}

function createChip(text, field) {
  const chip = document.createElement("div");
  chip.className = "chip";
  chip.textContent = text;
  chip.dataset.field = field;
  chip.addEventListener("click", toggleSelectLabel);
  return chip;
}

function createSelectable(text, field) {
  const tag = document.createElement("div");
  tag.className = "selectable";
  tag.textContent = text;
  tag.dataset.field = field;
  tag.addEventListener("click", toggleSelectLabel);
  return tag;
}

function populateTags() {
  // Traits
  const traitContainer = document.querySelector(
    ".chip-row[data-field='traits']"
  );
  traits.forEach((trait) => {
    traitContainer.appendChild(createChip(trait, "traits"));
  });

  // Badges
  const badgeContainer = document.querySelector(
    ".chip-row[data-field='badges']"
  );
  badges.forEach((badge) => {
    badgeContainer.appendChild(createChip(badge, "badges"));
  });

  // PlayType & Outcome
  const playSelect = document.querySelector("select[name='playtype']");
  const playPlaceholder = new Option("Play Type", "");
  playPlaceholder.className = "placeholder-option";
  playSelect.add(playPlaceholder);
  playTypes.forEach(({ label, value }) => {
    const option = new Option(label, value);
    playSelect.add(option);
  });

  const outcomeSelect = document.querySelector("select[name='outcome']");
  const outcomePlaceholder = new Option("Outcome", "");
  outcomePlaceholder.className = "placeholder-option";
  outcomeSelect.add(outcomePlaceholder);
  outcomes.forEach((opt) => {
    const option = new Option(opt, opt);
    outcomeSelect.add(option);
  });

  // Situation & Context
  const situationSelect = document.querySelector("select[name='situation']");
  const situationPlaceholder = new Option("Situation", "");
  situationPlaceholder.className = "placeholder-option";
  situationSelect.add(situationPlaceholder);
  situations.forEach(({ label, value }) => {
    const option = new Option(label, value);
    situationSelect.add(option);
  });

  const contextSelect = document.querySelector("select[name='context']");
  const contextPlaceholder = new Option("Context", "");
  contextPlaceholder.className = "placeholder-option";
  contextSelect.add(contextPlaceholder);
  contexts.forEach((opt) => {
    const option = new Option(opt, opt);
    contextSelect.add(option);
  });

  // Role selection
  const roleSelect = document.querySelector(
    "#roles-section select.role-select"
  );
  if (roleSelect) {
    const placeholder = new Option("Role", "");
    placeholder.className = "placeholder-option";
    roleSelect.add(placeholder);
    offensiveRoles.forEach((role) => {
      roleSelect.add(new Option(role, role));
    });

    const hiddenInput = document.querySelector("input[name='roles']");
    window.updateRoles = () => {
      hiddenInput.value = roleSelect.value || "";
    };

    roleSelect.addEventListener("change", window.updateRoles);
    // Initialize hidden value
    window.updateRoles();
  }

  // SubRoles with Positive/Negative sections
  const subroleList = document.querySelector("#subroles-section .tag-list");
  if (subroleList) {
    subroleList.innerHTML += "<div class='subrole-divider'>Positive</div>";
    offensiveSubrolesPositive.forEach((sub) =>
      subroleList.appendChild(createSelectable(sub, "subroles"))
    );
    subroleList.innerHTML += "<div class='subrole-divider'>Negative</div>";
    offensiveSubrolesNegative.forEach((sub) =>
      subroleList.appendChild(createSelectable(sub, "subroles"))
    );
  }
}

window.addEventListener("DOMContentLoaded", populateTags);
