
import "./style.css";

window.addEventListener("DOMContentLoaded", () => {
  // ✅ Create map AFTER DOM exists
  const map = L.map("map").setView([20, 0], 2);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  // ✅ Create WebSocket AFTER map exists
  const ws = new WebSocket("ws://127.0.0.1:8000/ws/traffic");

  ws.onopen = () => {
    console.log("Connected to backend");
  };
const markers = [];

function addMarker(marker) {
  markers.push(marker);
  if (markers.length > 1000) {
    map.removeLayer(markers.shift());
  }
}

ws.onmessage = (msg) => {
  const data = JSON.parse(msg.data);
  const m = data.metrics;
  const e = data.event;

  if (!m || !e || e.lat == null) return;

  document.getElementById("total").textContent = m.total_events;
  document.getElementById("ddos").textContent = m.ddos_events;
  document.getElementById("normal").textContent = m.normal_events;
  document.getElementById("eps").textContent = m.events_per_second;

  const color = e.label === "ddos" ? "red" : "green";

  const marker = L.circleMarker([e.lat, e.lon], {
    radius: 6,
    color,
    fillOpacity: 0.7
  }).addTo(map);

  addMarker(marker);
};

  ws.onerror = (err) => {
    console.error("WebSocket error", err);
  };
});

