async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json();
}

function renderTemplates(templates) {
  const container = document.getElementById("templates");
  container.innerHTML = "";

  templates.forEach((template) => {
    const item = document.createElement("div");
    item.className = "card";
    item.innerHTML = `
      <div class="card-head">
        <strong>${template.name}</strong>
        <span>${template.category}</span>
      </div>
      <p>${template.prompt}</p>
    `;
    container.appendChild(item);
  });
}

function renderVersions(versions) {
  const container = document.getElementById("versions");
  container.innerHTML = "";

  if (!versions.length) {
    container.innerHTML = "<p class='empty'>No saved versions yet.</p>";
    return;
  }

  versions.forEach((version) => {
    const item = document.createElement("div");
    item.className = "card";
    item.innerHTML = `
      <div class="card-head">
        <strong>${version.version} - ${version.title}</strong>
        <span>${version.metrics.overall}/100</span>
      </div>
      <p>${version.notes || "No notes provided."}</p>
      <code>${version.tags.join(", ") || "untagged"}</code>
    `;
    container.appendChild(item);
  });
}

function renderAnalytics(analytics) {
  const container = document.getElementById("analytics");
  container.innerHTML = `
    <div class="metric"><span>Runs</span><strong>${analytics.runs}</strong></div>
    <div class="metric"><span>Average Score</span><strong>${analytics.average_score}</strong></div>
    <div class="metric"><span>Average Time (ms)</span><strong>${analytics.average_duration_ms}</strong></div>
    <div class="metric"><span>Top Tags</span><strong>${(analytics.top_tags || []).map((tag) => tag.tag).join(", ") || "None"}</strong></div>
  `;
}

async function refresh() {
  const templates = await fetchJson("/api/templates");
  const versions = await fetchJson("/api/versions");
  const analytics = await fetchJson("/api/analytics");

  renderTemplates(templates.templates);
  renderVersions(versions.versions);
  renderAnalytics(analytics);
}

document.getElementById("enhanceButton").addEventListener("click", async () => {
  const prompt = document.getElementById("prompt").value;
  const goal = document.getElementById("goal").value;
  const audience = document.getElementById("audience").value;
  const constraints = document.getElementById("constraints").value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);

  const result = await fetchJson("/api/enhance", {
    method: "POST",
    body: JSON.stringify({ prompt, goal, audience, constraints }),
  });

  document.getElementById("enhancedOutput").textContent =
    `${result.enhanced}\n\nSuggestions:\n- ${result.suggestions.join("\n- ") || "No suggestions"}\n\nScore: ${result.metrics.overall}`;
  document.getElementById("versionPrompt").value = result.enhanced;
  await refresh();
});

document.getElementById("saveVersionButton").addEventListener("click", async () => {
  const title = document.getElementById("versionTitle").value;
  const prompt = document.getElementById("versionPrompt").value;
  const notes = document.getElementById("versionNotes").value;
  const tags = document.getElementById("versionTags").value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);

  await fetchJson("/api/versions", {
    method: "POST",
    body: JSON.stringify({ title, prompt, notes, tags }),
  });

  document.getElementById("versionTitle").value = "";
  document.getElementById("versionTags").value = "";
  document.getElementById("versionNotes").value = "";
  await refresh();
});

refresh().catch((error) => {
  document.getElementById("enhancedOutput").textContent = error.message;
});
