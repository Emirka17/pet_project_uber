// frontend/passenger-app/src/components/MapComponent.js
import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Исправляем иконки Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const DEFAULT_CENTER = [40.7128, -74.0060];
const DEFAULT_ZOOM = 13;

function MapComponent({ pickupLocation, dropoffLocation, onMapClick }) {
  // Дефолтные маркеры
  const pickupMarker = pickupLocation 
    ? [pickupLocation.lat || 40.7128, pickupLocation.lng || -74.0060]
    : null;
    
  const dropoffMarker = dropoffLocation 
    ? [dropoffLocation.lat || 40.7580, dropoffLocation.lng || -73.9855]
    : null;

  return (
    <div className="w-full h-80 rounded-lg overflow-hidden shadow-md border">
      <MapContainer
        center={DEFAULT_CENTER}
        zoom={DEFAULT_ZOOM}
        style={{ height: '100%', width: '100%' }}
        eventHandlers={{
          click: (e) => {
            console.log('Map clicked:', e.latlng); // Для отладки
            if (onMapClick) {
              onMapClick(e.latlng);
            }
          }
        }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {pickupMarker && (
          <Marker position={pickupMarker}>
            <Popup>
              <div className="font-semibold">Точка отправления</div>
              <div className="text-sm">Координаты: {pickupMarker[0].toFixed(6)}, {pickupMarker[1].toFixed(6)}</div>
            </Popup>
          </Marker>
        )}
        
        {dropoffMarker && (
          <Marker position={dropoffMarker}>
            <Popup>
              <div className="font-semibold">Точка назначения</div>
              <div className="text-sm">Координаты: {dropoffMarker[0].toFixed(6)}, {dropoffMarker[1].toFixed(6)}</div>
            </Popup>
          </Marker>
        )}
        
        {pickupMarker && dropoffMarker && (
          <Polyline
            positions={[pickupMarker, dropoffMarker]}
            color="#3b82f6"
            weight={4}
          />
        )}
      </MapContainer>
    </div>
  );
}

export default MapComponent;
