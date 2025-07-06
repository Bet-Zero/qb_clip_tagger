const offensiveRoles = [
  "Primary Playmaker",
  "Primary Ball Handler",
  "Secondary Creator",
  "Scorer",
  "Shooter",
  "Floor Spacer",
  "Off-Ball Scorer",
  "Off-Ball Mover",
  "Connector",
  "Versatile Big",
  "Post Hub",
  "Post Scorer",
  "Stretch Big",
  "Play Finisher",
];

const defensiveRoles = [
  "Point-of-Attack Defender",
  "Chaser",
  "Wing Stopper",
  "Off-Ball Helper",
  "Defensive Playmaker",
  "Defensive Quarterback",
  "Switchable Wing",
  "Switchable Big",
  "Mobile Big",
  "Post Defender",
  "Anchor Big",
];

const offensiveSubrolesPositive = [
  "Short Roll Creator",
  "Pick & Pop Threat",
  "Isolation Creator",
  "Post Scorer",
  "Spot-Up Weapon",
  "Slashing Threat",
  "Lob Threat",
  "Transition Finisher",
  "Connector",
  "Cutter",
  "Movement Shooter",
  "Mismatch Hunter",
  "Pushes in Transition",
  "Quick Decision Maker",
  "Roll Gravity",
  "And-One Finisher",
];

const offensiveSubrolesNegative = [
  "Ball Stops",
  "Low Feel",
  "Tunnel Vision",
  "Inefficient Usage",
  "Bad Shot Selection",
  "Overdribbles",
  "Poor Spacing",
  "Turnover Prone",
  "No Off-Ball Impact",
  "Low Activity",
  "Wild Drives",
  "Avoids Contact",
  "Slow to Read",
  "Wasted Dribbles",
  "Forces into Crowds",
];

const defensiveSubrolesPositive = [
  "Point of Attack Stopper",
  "Off-Ball Navigator",
  "Screen Navigator",
  "Shot Contester",
  "Rotational Help",
  "Event Creator",
  "Switch Defender",
  "Anchor Big",
  "Tag & Recover",
  "Communicator",
  "Rebound & Run",
  "Defensive Quarterback",
  "Stunt & Recover",
  "Paint Presence",
  "Charge Taker",
];

const defensiveSubrolesNegative = [
  "Ball Watcher",
  "Slow to Rotate",
  "Foul Prone",
  "Poor Contests",
  "Struggles in Space",
  "Late on Help",
  "Bad Closeouts",
  "Easily Screened",
  "No Second Effort",
  "Loses Matchups",
  "Poor Communicator",
  "Misses Rotations",
  "Overhelps",
  "Underhelps",
  "No Shot Blocking",
];

const traits = [
  "Defense",
  "Shooting",
  "Playmaking",
  "Passing",
  "Rebounding",
  "IQ",
  "Feel",
  "Energy",
];

const badges = [
  "Sniper",
  "Dimes",
  "Bucket",
  "Handles",
  "Board Man",
  "High Flyer",
  "Bully",
  "Speed",
  "Floor General",
  "Clutch",
  "High Motor",
  "High IQ",
  "Coach's Dream",
  "Versatile",
  "Chess Piece",
  "Dog",
  "Leader",
  "Lockdown Defender",
  "Glue Guy",
  "Disruptor",
  "Mismatch Nightmare",
  "Iron Man",
  "Cool Under Pressure",
  "Veteran Presence",
];

const playTypes = [
  "Spot-Up Jumper",
  "Catch & Drive",
  "Pump Fake Drive",
  "Spin Move",
  "Eurostep",
  "Stepback Jumper",
  "Pull-Up Jumper",
  "Layup",
  "Dunk",
  "Hook Shot",
  "Kickout Pass",
  "Dump-Off",
  "Entry Pass",
  "Skip Pass",
  "Touch Pass",
  "Closeout",
  "Recovery Contest",
  "Tag & Recover",
  "Late Rotation",
  "Isolation",
  "Pick & Roll Ball Handler",
  "Pick & Roll Roll Catch",
  "Pick & Roll Pop",
  "Off-Screen Action",
  "Transition",
  "Scramble Rotation",
  "Post Entry",
  "Rebound Putback",
  "Kickout Attack",
  "Handoff Action",
  "Inbound Play",
];

const outcomes = [
  "Make",
  "Miss",
  "Foul",
  "TO",
  "AST",
  "BLK",
  "And1",
  "Deflect",
  "ForceMiss",
  "BlowRot",
  "Charge",
  "Steal",
];

const situations = [
  "Isolation",
  "Pick & Roll Ball Handler",
  "Pick & Roll Roll Catch",
  "Pick & Roll Pop",
  "Off-Screen Action",
  "Transition",
  "Scramble Rotation",
  "Post Entry",
  "Rebound Putback",
  "Inbound Play",
];

const contexts = ["1Q", "2Q", "3Q", "4Q", "OT"];

function createChip(text, field) {
  const chip = document.createElement("div");
  chip.className = "chip";
  chip.textContent = text;
  chip.dataset.field = field;
  chip.onclick = toggleSelectLabel;
  return chip;
}

function createSelectable(text, field) {
  const tag = document.createElement("div");
  tag.className = "selectable";
  tag.textContent = text;
  tag.dataset.field = field;
  tag.onclick = toggleSelectLabel;
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
  playTypes.forEach((opt) => {
    const option = new Option(opt, opt);
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
  situations.forEach((opt) => {
    const option = new Option(opt, opt);
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

  // Roles (Offense & Defense)
  const roleSelects = document.querySelectorAll(
    "#roles-section select.role-select"
  );
  if (roleSelects.length >= 2) {
    const [offenseSelect, defenseSelect] = roleSelects;
    const offensePlaceholder = new Option("Offense Role", "");
    offensePlaceholder.className = "placeholder-option";
    offenseSelect.add(offensePlaceholder);
    const defensePlaceholder = new Option("Defense Role", "");
    defensePlaceholder.className = "placeholder-option";
    defenseSelect.add(defensePlaceholder);
    offensiveRoles.forEach((role) => {
      offenseSelect.add(new Option(role, role));
    });
    defensiveRoles.forEach((role) => {
      defenseSelect.add(new Option(role, role));
    });

    const hiddenInput = document.querySelector("input[name='roles']");
    window.updateRoles = () => {
      const selected = [offenseSelect.value, defenseSelect.value].filter(
        Boolean
      );
      hiddenInput.value = selected.join(",");
    };

    offenseSelect.addEventListener("change", window.updateRoles);
    defenseSelect.addEventListener("change", window.updateRoles);
    // Initialize hidden value
    window.updateRoles();
  }

  // SubRoles (Offense & Defense, with Positive/Negative sections)
  const subroleLists = document.querySelectorAll("#subroles-section .tag-list");
  if (subroleLists.length >= 2) {
    const [offenseList, defenseList] = subroleLists;

    offenseList.innerHTML += "<div class='subrole-divider'>Positive</div>";
    offensiveSubrolesPositive.forEach((sub) =>
      offenseList.appendChild(createSelectable(sub, "subroles"))
    );
    offenseList.innerHTML += "<div class='subrole-divider'>Negative</div>";
    offensiveSubrolesNegative.forEach((sub) =>
      offenseList.appendChild(createSelectable(sub, "subroles"))
    );

    defenseList.innerHTML += "<div class='subrole-divider'>Positive</div>";
    defensiveSubrolesPositive.forEach((sub) =>
      defenseList.appendChild(createSelectable(sub, "subroles"))
    );
    defenseList.innerHTML += "<div class='subrole-divider'>Negative</div>";
    defensiveSubrolesNegative.forEach((sub) =>
      defenseList.appendChild(createSelectable(sub, "subroles"))
    );
  }
}

window.addEventListener("DOMContentLoaded", populateTags);
