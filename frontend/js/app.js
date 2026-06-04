// ─── API base — change to your Render URL when deployed ───
// const API_BASE = "http://localhost:5000";
const API_BASE = "https://ecogacha-xxxx.onrender.com";

async function api(path, method = "GET", body = null) {
  const opts = { method, headers: { "Content-Type": "application/json" } };
  if (body) opts.body = JSON.stringify(body);
  try {
    const res = await fetch(`${API_BASE}${path}`, opts);
    return await res.json();
  } catch (e) {
    return { error: "Network error — is the backend running?" };
  }
}

function requireAuth() {
  const raw = localStorage.getItem("student");
  if (!raw) { window.location.href = "index.html"; return null; }
  return JSON.parse(raw);
}

function logout() {
  localStorage.removeItem("student");
  window.location.href = "index.html";
}

function capitalize(str) {
  if (!str) return "";
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString("en-NG", { day: "numeric", month: "short", year: "numeric" });
}

// ─── Theme toggle (persisted in localStorage) ───
function initTheme() {
  const saved = localStorage.getItem("theme") || "dark";
  applyTheme(saved);
}

function applyTheme(theme) {
  document.body.classList.toggle("light", theme === "light");
  const btn = document.getElementById("theme-toggle");
  if (btn) btn.textContent = theme === "light" ? "🌙" : "☀️";
  localStorage.setItem("theme", theme);
}

function toggleTheme() {
  const current = localStorage.getItem("theme") || "dark";
  applyTheme(current === "dark" ? "light" : "dark");
}

// Run theme init on every page load
document.addEventListener("DOMContentLoaded", initTheme);
