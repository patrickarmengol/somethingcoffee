const copy =
  "© <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors";
const url = "https://tile.openstreetmap.org/{z}/{x}/{y}.png";
const osm = L.tileLayer(url, { attribution: copy });
const map = L.map("map", { layers: [osm], minZoom: 5 });
map.setView([35.68, 139.76], 13);

async function load_markers() {
  const markers_url = `/shops/geojson`;
  const response = await fetch(markers_url);
  const geojson = await response.json();
  return geojson;
}

async function render_markers() {
  const markers = await load_markers();
  L.geoJSON(markers)
    .bindPopup((layer) => layer.feature.properties.name)
    .addTo(map);
}

render_markers();
