// frontend/passenger-app/src/pages/OrderPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import MapComponent from '../components/MapComponent';

function OrderPage() {
  const navigate = useNavigate();
  
  const [pickupLocation, setPickupLocation] = useState({
    address: 'Точка отправления',
    lat: 40.7128,
    lng: -74.0060
  });
  
  const [dropoffLocation, setDropoffLocation] = useState({
    address: 'Точка назначения',
    lat: 40.7580,
    lng: -73.9855
  });
  
  const [isLoading, setIsLoading] = useState(false);
  const [activeInput, setActiveInput] = useState('pickup');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      console.log('Заказ:', { pickupLocation, dropoffLocation });
      await new Promise(resolve => setTimeout(resolve, 1000));
      navigate('/tracking');
    } catch (error) {
      console.error('Ошибка:', error);
      alert('Произошла ошибка');
    } finally {
      setIsLoading(false);
    }
  };

  const handleMapClick = (latlng) => {
    console.log('OrderPage - Map clicked:', latlng); // Для отладки
    
    if (activeInput === 'pickup') {
      setPickupLocation({
        address: `Координаты: ${latlng.lat.toFixed(6)}, ${latlng.lng.toFixed(6)}`,
        lat: latlng.lat,
        lng: latlng.lng
      });
      console.log('Set pickup location:', latlng);
    } else {
      setDropoffLocation({
        address: `Координаты: ${latlng.lat.toFixed(6)}, ${latlng.lng.toFixed(6)}`,
        lat: latlng.lat,
        lng: latlng.lng
      });
      console.log('Set dropoff location:', latlng);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">🚖 Заказ поездки</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Информация о поездке</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Точка отправления
              </label>
              <input
                type="text"
                value={pickupLocation.address}
                onChange={(e) => setPickupLocation({...pickupLocation, address: e.target.value})}
                onFocus={() => setActiveInput('pickup')}
                placeholder="Введите адрес отправления"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Точка назначения
              </label>
              <input
                type="text"
                value={dropoffLocation.address}
                onChange={(e) => setDropoffLocation({...dropoffLocation, address: e.target.value})}
                onFocus={() => setActiveInput('dropoff')}
                placeholder="Введите адрес назначения"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            
            <div className="bg-blue-50 p-3 rounded-md">
              <div className="text-sm text-blue-800">
                <div>📍 Отправление: {pickupLocation.lat.toFixed(6)}, {pickupLocation.lng.toFixed(6)}</div>
                <div>🏁 Назначение: {dropoffLocation.lat.toFixed(6)}, {dropoffLocation.lng.toFixed(6)}</div>
              </div>
            </div>
            
            <div className="pt-4">
              <button
                type="submit"
                disabled={isLoading}
                className="w-full button-primary flex items-center justify-center"
              >
                {isLoading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Создание заказа...
                  </>
                ) : (
                  'Заказать поездку'
                )}
              </button>
            </div>
          </form>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Карта маршрута</h2>
          <div className="mb-2 text-sm text-gray-600">
            {activeInput === 'pickup' 
              ? '👆 Кликните на карту, чтобы выбрать точку отправления' 
              : '👆 Кликните на карту, чтобы выбрать точку назначения'}
          </div>
          <MapComponent 
            pickupLocation={pickupLocation}
            dropoffLocation={dropoffLocation}
            onMapClick={handleMapClick}
          />
        </div>
      </div>
    </div>
  );
}

export default OrderPage;
