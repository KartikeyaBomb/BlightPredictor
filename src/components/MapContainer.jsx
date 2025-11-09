import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { useRef, useEffect, useState } from "react";

function MapContainer() {
  const mapRef = useRef(null);
  const mapContainerRef = useRef(null);

  const [modalOpen, setModalOpen] = useState(false);
  const [selectedZip, setSelectedZip] = useState(null);

  useEffect(() => {
    if (mapRef.current) return;

    mapboxgl.accessToken =
      "pk.eyJ1IjoiYm9ta2EiLCJhIjoiY21ocXZuendlMTB1MTJqcHpqamx3NzVrciJ9.LnpWZyAtsFMkWzRbOyMkKw";

    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/bomka/cmhqv52hy005d01r0h3udd541",
      center: [-90.049, 35.146],
      zoom: 10,
    });
    mapRef.current = map;

    map.on("load", async () => {
      const geo = await fetch("/memphis.json").then((r) => r.json());

      map.addSource("memphis", {
        type: "geojson",
        data: geo,
      });

      const redZips = ["38128", "38127", "38118", "38114"];

      map.addLayer({
        id: "memphis-fill",
        type: "fill",
        source: "memphis",
        paint: {
          "fill-color": "#ffffff",
          "fill-opacity": 0.2,
        },
      });

      map.addLayer({
        id: "hot-zips",
        type: "fill",
        source: "memphis",
        paint: {
          "fill-color": "#ff0000",
          "fill-opacity": 0.5,
        },
        filter: ["in", ["to-string", ["get", "Name"]], ["literal", redZips]],
      });

      map.addLayer({
        id: "memphis-outline",
        type: "line",
        source: "memphis",
        paint: {
          "line-color": "#333",
          "line-width": 1.5,
        },
      });

      map.on("mouseenter", "hot-zips", () => {
        map.getCanvas().style.cursor = "pointer";
      });
      map.on("mouseleave", "hot-zips", () => {
        map.getCanvas().style.cursor = "";
      });

      map.on("click", "hot-zips", (e) => {
        const zip = e.features[0].properties.Name;
        setSelectedZip(zip);
        setModalOpen(true);
      });

      const bounds = new mapboxgl.LngLatBounds();
      geo.features.forEach((f) => {
        const coords =
          f.geometry.type === "Polygon"
            ? f.geometry.coordinates.flat(1)
            : f.geometry.type === "MultiPolygon"
            ? f.geometry.coordinates.flat(2)
            : [];
        coords.forEach((c) => bounds.extend([c[0], c[1]]));
      });
      map.fitBounds(bounds, { padding: 40 });
    });

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  return (
    <>
      <div ref={mapContainerRef} style={{ width: "100%", height: "100vh" }} />

      {modalOpen && (
        <div
          style={{
            position: "fixed",
            inset: 0,
            background: "rgba(0,0,0,0.6)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 999,
          }}
          onClick={() => setModalOpen(false)}
        >
          <div
            style={{
              width: "80vw",
              height: "80vh",
              background: "white",
              borderRadius: "8px",
              padding: "20px",
              position: "relative",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setModalOpen(false)}
              style={{
                position: "absolute",
                top: 10,
                right: 10,
                padding: "5px 10px",
                cursor: "pointer",
              }}
            >
              Back to Map
            </button>

            <h1>{selectedZip}</h1>
          </div>
        </div>
      )}
    </>
  );
}

export default MapContainer;
