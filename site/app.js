// app.js - runs on the home page (index.html).
// It does two jobs:
//   1. Reads games.json and shows a card for each game.
//   2. Sends the suggestion form in the background, so the page doesn't reload.

// ---------- 1. Game cards ----------

async function loadGames() {
  const grid = document.getElementById("game-grid");
  try {
    const response = await fetch("games.json");   // ask the server for the list
    const games = await response.json();          // turn the text into JS objects

    grid.innerHTML = "";                           // clear "Loading games..."
    for (const game of games) {
      grid.insertAdjacentHTML("beforeend", makeCard(game));
    }

    // Update the little numbers in the intro
    const live = games.filter(g => g.status === "playable").length;
    document.getElementById("stat-live").textContent = live;
    document.getElementById("stat-progress").textContent = games.length - live;
  } catch (error) {
    grid.innerHTML = `<p class="muted">Couldn't load the games list. Try refreshing the page.</p>`;
    console.error(error);
  }
}

// Builds the HTML for one card. (games.json is written by us, so it's safe
// to put its text straight into HTML.)
function makeCard(game) {
  const tags = game.tags.map(tag => `<span class="tag">${tag}</span>`).join("");

  // A game that isn't finished yet gets a placeholder and no Play button
  if (game.status !== "playable") {
    return `
      <article class="card upcoming">
        <div class="thumb placeholder"><span>In development</span></div>
        <div class="card-body">
          <div class="tags">${tags}</div>
          <h3>${game.title}</h3>
          <p>${game.description}</p>
          <span class="badge">Coming soon</span>
        </div>
      </article>`;
  }

  const link = `play.html?id=${encodeURIComponent(game.id)}`;
  return `
    <article class="card">
      <a class="thumb" href="${link}" tabindex="-1" aria-hidden="true">
        <img src="${game.thumbnail}" alt="" loading="lazy">
      </a>
      <div class="card-body">
        <div class="tags">${tags}</div>
        <h3><a href="${link}">${game.title}</a></h3>
        <p>${game.description}</p>
        <a class="btn primary small" href="${link}">Play &#9656;</a>
      </div>
    </article>`;
}

// ---------- 2. Suggestion form ----------

const form = document.getElementById("suggest-form");
const statusText = form.querySelector(".form-status");
const button = form.querySelector("button");

form.addEventListener("submit", async (event) => {
  event.preventDefault();               // stop the browser's normal page reload
  button.disabled = true;
  showStatus("Sending...", "");

  // Netlify wants the form data in "URL-encoded" format: idea=...&genre=...
  const body = new URLSearchParams(new FormData(form)).toString();

  try {
    const response = await fetch("/", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body,
    });
    if (!response.ok) throw new Error("Server said " + response.status);
    form.reset();
    showStatus("Thanks! Your idea was sent.", "ok");
  } catch (error) {
    const onMyComputer = ["localhost", "127.0.0.1"].includes(location.hostname);
    showStatus(
      onMyComputer
        ? "The suggestion box only works on the live (deployed) site."
        : "Sorry, that didn't send. Please try again in a moment.",
      "error"
    );
    console.error(error);
  } finally {
    button.disabled = false;
  }
});

function showStatus(message, state) {
  statusText.textContent = message;
  statusText.dataset.state = state;     // used by the CSS to pick a colour
}

loadGames();
