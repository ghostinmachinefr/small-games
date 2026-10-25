// play.js - runs on play.html.
// Reads which game to show from the address (play.html?id=snake),
// looks it up in games.json, and loads it into the iframe.

async function loadGame() {
  const id = new URLSearchParams(location.search).get("id");
  const titleEl = document.getElementById("title");

  const games = await (await fetch("games.json")).json();
  const game = games.find(g => g.id === id && g.status === "playable");

  if (!game) {
    titleEl.textContent = "Game not found";
    document.querySelector(".stage").remove();
    document.querySelector(".player-bar").remove();
    document.querySelector(".controls").remove();
    return;
  }

  document.title = `${game.title} · Small Games`;
  titleEl.textContent = game.title;
  document.getElementById("description").textContent = game.description;

  // Keep the game's shape (e.g. 600 x 520) so it isn't stretched.
  // The CSS uses --ratio to size the frame.
  const frame = document.getElementById("frame");
  frame.style.setProperty("--ratio", game.width / game.height);

  document.getElementById("game").src = game.path;

  const list = document.getElementById("controls");
  for (const line of game.controls) {
    const item = document.createElement("li");
    item.textContent = line;
    list.appendChild(item);
  }
}

// Keyboard focus: keys only reach the game when the iframe is "focused".
// Focus it as soon as it loads, and if a game key is pressed while the
// outer page has focus, stop the page scrolling and hand focus to the game.
const iframe = document.getElementById("game");
iframe.addEventListener("load", () => iframe.focus());

const GAME_KEYS = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "];
window.addEventListener("keydown", (event) => {
  if (GAME_KEYS.includes(event.key)) {
    event.preventDefault();
    iframe.focus();
  }
});

// Full screen button: asks the browser to make the game fill the screen
document.getElementById("fullscreen").addEventListener("click", () => {
  const frame = document.getElementById("frame");
  if (frame.requestFullscreen) frame.requestFullscreen();
});

loadGame();
