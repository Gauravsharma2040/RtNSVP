// Helper for fake coordinates
import "./style.css";
function fakeGeo() {
  return [
    Math.random() * 180 - 90,
    Math.random() * 360 - 180
  ];
}

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

  ws.onmessage = (msg) => {
    const data = JSON.parse(msg.data);
    const m = data.metrics;
    if (!m) return;

    // Update metrics
    document.getElementById("total").textContent = m.total_events;
    document.getElementById("ddos").textContent = m.ddos_events;
    document.getElementById("normal").textContent = m.normal_events;
    document.getElementById("eps").textContent = m.events_per_second;

    // Plot event
    const coords = fakeGeo();
    const color = data.event.label === "ddos" ? "red" : "green";

    const marker = L.circleMarker(coords, {
      radius: 6,
      color,
      fillOpacity: 0.8,
    }).addTo(map);

    // Auto-remove marker
    setTimeout(() => {
      map.removeLayer(marker);
    }, 10000);
  };

  ws.onerror = (err) => {
    console.error("WebSocket error", err);
  };
});

