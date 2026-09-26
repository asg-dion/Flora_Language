const petalLayer = document.querySelector("#petal-weather");
const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");
const petals = [];
const petalTimers = new WeakMap();

function randomBetween(minimum, maximum) {
  return Math.random() * (maximum - minimum) + minimum;
}

function scatterPetal(petal) {
  petal.style.animation = "none";
  petal.style.left = `${randomBetween(4, 96)}vw`;
  petal.style.top = `${randomBetween(5, 90)}vh`;
  petal.style.opacity = randomBetween(0.38, 0.5).toFixed(2);
  petal.style.transform = `rotate(${randomBetween(-55, 55).toFixed(0)}deg)`;
}

function animatePetal(petal, beginInProgress = false) {
  const timer = petalTimers.get(petal);
  if (timer) {
    clearTimeout(timer);
    petalTimers.delete(petal);
  }

  if (motionPreference.matches) {
    scatterPetal(petal);
    return;
  }

  const duration = randomBetween(24, 34);
  const initialProgress = beginInProgress ? randomBetween(0.12, 0.72) : 0;
  petal.style.left = `${randomBetween(4, 96)}vw`;
  petal.style.width = `${randomBetween(20, 30).toFixed(0)}px`;
  petal.style.opacity = "";
  petal.style.setProperty("--petal-opacity", randomBetween(0.48, 0.62).toFixed(2));
  petal.style.setProperty("--drift-one", `${randomBetween(-34, 34).toFixed(0)}px`);
  petal.style.setProperty("--drift-two", `${randomBetween(-46, 46).toFixed(0)}px`);
  petal.style.setProperty("--drift-end", `${randomBetween(-28, 28).toFixed(0)}px`);
  petal.style.setProperty("--turn-one", `${randomBetween(-45, 45).toFixed(0)}deg`);
  petal.style.setProperty("--turn-two", `${randomBetween(-110, 110).toFixed(0)}deg`);
  petal.style.setProperty("--turn-end", `${randomBetween(-180, 180).toFixed(0)}deg`);
  petal.style.animation = "none";
  void petal.offsetWidth;
  petal.style.animation = `petal-fall ${duration}s linear ${-duration * initialProgress}s 1 both`;
  petal.onanimationend = () => {
    if (motionPreference.matches) {
      return;
    }
    const restartTimer = setTimeout(
      () => animatePetal(petal),
      randomBetween(300, 1200),
    );
    petalTimers.set(petal, restartTimer);
  };
}

for (let index = 0; index < 9; index += 1) {
  const petal = document.createElement("img");
  petal.className = "weather-petal";
  petal.src = "/assets/petal.png";
  petal.alt = "";
  petalLayer.append(petal);
  petals.push(petal);
  animatePetal(petal, true);
}

motionPreference.addEventListener("change", () => {
  for (const petal of petals) {
    if (motionPreference.matches) {
      const timer = petalTimers.get(petal);
      if (timer) {
        clearTimeout(timer);
        petalTimers.delete(petal);
      }
      scatterPetal(petal);
    } else {
      animatePetal(petal, true);
    }
  }
});

const petalFallStyles = document.createElement("style");
petalFallStyles.textContent = `
  @keyframes petal-fall {
    0% {
      opacity: 0;
      transform: translate3d(0, -6vh, 0) rotate(0deg);
    }
    12% {
      opacity: var(--petal-opacity);
    }
    38% {
      transform: translate3d(var(--drift-one), 32vh, 0) rotate(var(--turn-one));
    }
    68% {
      transform: translate3d(var(--drift-two), 72vh, 0) rotate(var(--turn-two));
    }
    86% {
      opacity: var(--petal-opacity);
    }
    100% {
      opacity: 0;
      transform: translate3d(var(--drift-end), 108vh, 0) rotate(var(--turn-end));
    }
  }
`;
document.head.append(petalFallStyles);

const backgroundMusic = new Audio("/sfx/background.mp3");
backgroundMusic.loop = true;
backgroundMusic.volume = 0.25;
backgroundMusic.preload = "auto";

const trainSound = new Audio("/sfx/choochoo.mp3");
trainSound.volume = 0.45;
trainSound.preload = "auto";
trainSound.loop = false;

const buttonSound = new Audio("/sfx/pop.mp3");
buttonSound.volume = 0.25;
buttonSound.preload = "auto";
buttonSound.load();

const audioToggle = document.querySelector("#audio-toggle");
const audioWaves = audioToggle.querySelector(".audio-icon-waves");
const audioMutedIcon = audioToggle.querySelector(".audio-icon-muted");
const train = document.querySelector(".footer-train");
let backgroundPlaybackPending = false;
let initialTrainSoundPending = true;

function removeAudioUnlockListeners() {
  document.removeEventListener("pointerdown", startBackgroundMusic);
  document.removeEventListener("keydown", startBackgroundMusic);
}

function startBackgroundMusic() {
  if (!backgroundMusic.paused || backgroundPlaybackPending) {
    return;
  }

  backgroundPlaybackPending = true;
  backgroundMusic.play()
    .then(() => {
      removeAudioUnlockListeners();
      playInitialTrainSound();
    })
    .catch(() => {})
    .finally(() => {
      backgroundPlaybackPending = false;
    });
}

document.addEventListener("pointerdown", startBackgroundMusic);
document.addEventListener("keydown", startBackgroundMusic);

audioToggle.addEventListener("click", () => {
  backgroundMusic.muted = !backgroundMusic.muted;
  const isMuted = backgroundMusic.muted;
  trainSound.muted = isMuted;
  audioToggle.classList.toggle("is-muted", isMuted);
  audioToggle.setAttribute("aria-pressed", String(isMuted));
  audioToggle.setAttribute("aria-label", `${isMuted ? "Unmute" : "Mute"} audio`);
  audioToggle.title = `${isMuted ? "Unmute" : "Mute"} audio`;
  audioWaves.hidden = isMuted;
  audioMutedIcon.hidden = !isMuted;
});

function playTrainSound() {
  trainSound.currentTime = 0;
  trainSound.play().catch(() => {});
}

function playInitialTrainSound() {
  if (!initialTrainSoundPending) {
    return;
  }

  initialTrainSoundPending = false;
  trainSound.currentTime = 0;
  trainSound.play().catch(() => {
    initialTrainSoundPending = true;
  });
}

playInitialTrainSound();
startBackgroundMusic();
train.addEventListener("click", playTrainSound);

const editor = document.querySelector(".editor-surface textarea");
const runButton = document.querySelector("#run-button");
const clearButton = document.querySelector("#clear-button");
const runStatus = document.querySelector("#run-status");
const statusIndicator = document.querySelector(".ready-indicator");
const examplesMenu = document.querySelector("#examples-menu");
const lineNumbers = document.querySelector("#line-numbers");
const consoleSurface = document.querySelector(".console-surface");
const consoleEmpty = document.querySelector("#console-empty");
const consoleOutput = document.querySelector("#console-output");
const errorSection = document.querySelector(".error-section");
const errorOutput = document.querySelector("#error-output");

function fitConsoleSurface() {
  consoleSurface.classList.toggle("is-expanded", consoleOutput.scrollHeight > 130);
}

const examples = {
  variables: `sprout root trees = 10;
sprout dew rainfall = 3.5;
bloom trees;
bloom rainfall;`,
  arithmetic: `sprout root trees = 10;
sprout root saplings = 5;
bloom trees + saplings;`,
  branch: `sprout root trees = 10;
branch(trees > 5)
bloom "Forest is thriving";`,
};

const codeHighlight = document.querySelector("#code-highlight");
const floraTokenPattern = /"[^\"]*"|\b(?:sprout|bloom|branch)\b|\b(?:root|dew|petal)\b|\b\d+(?:\.\d+)?\b/g;

function escapeCodeText(text) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderHighlight(source) {
  let html = "";
  let previousEnd = 0;

  for (const match of source.matchAll(floraTokenPattern)) {
    const token = match[0];
    const start = match.index;
    html += escapeCodeText(source.slice(previousEnd, start));

    let tokenClass = "";
    if (token.startsWith('"')) {
      tokenClass = "token-string";
    } else if (/^(sprout|bloom|branch)$/.test(token)) {
      tokenClass = "token-keyword";
    } else if (/^(root|dew|petal)$/.test(token)) {
      tokenClass = "token-type";
    } else {
      tokenClass = "token-number";
    }

    html += `<span class="${tokenClass}">${escapeCodeText(token)}</span>`;
    previousEnd = start + token.length;
  }

  codeHighlight.innerHTML = html + escapeCodeText(source.slice(previousEnd));
}

function updateLineNumbers() {
  const count = editor.value.split("\n").length;
  lineNumbers.replaceChildren();

  for (let index = 1; index <= count; index += 1) {
    const number = document.createElement("span");
    number.textContent = index;
    lineNumbers.append(number);
  }

  renderHighlight(editor.value);
}

editor.addEventListener("input", updateLineNumbers);
editor.addEventListener("scroll", () => {
  codeHighlight.scrollTop = editor.scrollTop;
  codeHighlight.scrollLeft = editor.scrollLeft;
  lineNumbers.scrollTop = editor.scrollTop;
});
updateLineNumbers();

document.querySelectorAll("[data-example]").forEach((button) => {
  button.addEventListener("click", () => {
    editor.value = examples[button.dataset.example];
    updateLineNumbers();
    examplesMenu.open = false;
    consoleEmpty.hidden = false;
    consoleOutput.hidden = true;
    consoleOutput.replaceChildren();
    errorSection.hidden = true;
    editor.focus();
  });
});

function renderOutput(lines) {
  consoleOutput.replaceChildren();
  consoleOutput.classList.remove("is-error");
  consoleEmpty.hidden = true;
  consoleOutput.hidden = false;
  errorSection.hidden = false;

  if (lines.length === 0) {
    consoleOutput.textContent = "No output from this bloom.";
    fitConsoleSurface();
    return;
  }

  lines.forEach((line, index) => {
    const outputLine = document.createElement("span");
    outputLine.className = "console-line";
    outputLine.style.setProperty("--line-index", index);
    outputLine.textContent = line;
    consoleOutput.append(outputLine);
  });
  fitConsoleSurface();
}

function renderError(errorType, message) {
  const fullMessage = `${errorType}: ${message}`;
  consoleOutput.replaceChildren();
  consoleOutput.classList.add("is-error");
  consoleEmpty.hidden = true;
  consoleOutput.hidden = false;
  errorSection.hidden = false;
  consoleOutput.textContent = fullMessage;
  errorOutput.textContent = "See console output above.";
  errorOutput.classList.add("has-error");
  fitConsoleSurface();
}

function resetWorkspace() {
  editor.value = "";
  updateLineNumbers();
  consoleEmpty.hidden = false;
  consoleOutput.hidden = true;
  consoleOutput.replaceChildren();
  consoleOutput.classList.remove("is-error");
  errorSection.hidden = true;
  consoleSurface.classList.remove("is-expanded");
  errorOutput.textContent = "Nothing caught this bloom.";
  errorOutput.classList.remove("has-error");
  runStatus.textContent = "READY";
  delete statusIndicator.dataset.state;
  editor.focus();
}

clearButton.addEventListener("click", resetWorkspace);

function playButtonSound() {
  buttonSound.currentTime = 0;
  buttonSound.play().catch(() => {});
}

runButton.addEventListener("click", playButtonSound);
clearButton.addEventListener("click", playButtonSound);

runButton.addEventListener("click", async () => {
  runButton.disabled = true;
  runButton.setAttribute("aria-busy", "true");
  runStatus.textContent = "RUNNING";
  statusIndicator.dataset.state = "running";
  consoleOutput.replaceChildren();
  consoleOutput.classList.remove("is-error");
  consoleEmpty.hidden = true;
  consoleOutput.hidden = true;
  errorSection.hidden = true;
  consoleSurface.classList.remove("is-expanded");
  errorOutput.textContent = "Bloom in progress.";
  errorOutput.classList.remove("has-error");

  try {
    const response = await fetch("/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source: editor.value }),
    });
    const result = await response.json();

    if (result.success) {
      renderOutput(result.output);
      errorOutput.textContent = "Nothing caught this bloom.";
    } else {
      renderError(result.error_type, result.message);
    }
  } catch (error) {
    renderError("Runtime Error", error.message);
  } finally {
    runButton.disabled = false;
    runButton.removeAttribute("aria-busy");
    runStatus.textContent = "READY";
    delete statusIndicator.dataset.state;
  }
});
