import { useRef, useEffect } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

function MapContainer({ 
  accessToken, 
  mapStyle, 
  center, 
  zoom, 
  onMapLoad,
  width = "100%",
  height = "100vh",
  style = {}
}) {
  const mapRef = useRef(null);
  const mapContainerRef = useRef(null);

  useEffect(() => {
    if (mapRef.current) return;

    mapboxgl.accessToken = accessToken;

    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: mapStyle,
      center: center,
      zoom: zoom,
    });
    mapRef.current = map;

    if (onMapLoad) {
      map.on("load", () => onMapLoad(map));
    }

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, [accessToken, mapStyle, center, zoom, onMapLoad]);

  return (
    <div 
      ref={mapContainerRef} 
      style={{ 
        width, 
        height,
        ...style
      }} 
    />
  );
}

export default MapContainer;
