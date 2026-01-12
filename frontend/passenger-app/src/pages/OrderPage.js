// Страница заказа поездки с интеграцией Ride Service
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import MapComponent from '../components/MapComponent';
import apiService from '../services/api';

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
  const [priceInfo, setPriceInfo] = useState(null);
  const [nearbyDrivers, setNearbyDrivers] = useState([]);
  const [error, setError] = useState('');

  // Обработка клика по карте
  const handleMapClick = (latlng) => {
    console.log('Map clicked:', latlng);
    
    if (activeInput === 'pickup') {
      setPickupLocation({
        address: `Координаты: ${latlng.lat.toFixed(6)}, ${latlng.lng.toFixed(6)}`,
        lat: latlng.lat,
        lng: latlng.lng
      });
    } else {
      setDropoffLocation({
        address: `Координаты: ${latlng.lat.toFixed(6)}, ${latlng.lng.toFixed(6)}`,
        lat: latlng.lat,
        lng: latlng.lng
      });
    }
  };

  // Расчет стоимости поездки
  const calculatePrice = async () => {
    if (!pickupLocation.lat || !dropoffLocation.lat) return;
    
    try {
      const pricingData = {
        pickup_latitude: pickupLocation.lat,
        pickup_longitude: pickupLocation.lng,
        dropoff_latitude: dropoffLocation.lat,
        dropoff_longitude: dropoffLocation.lng,
        passenger_count: 1,
        pickup_datetime: new Date().toISOString()
      };
      
      console.log('Calculating price:', pricingData);
      const priceResult = await apiService.calculatePrice(pricingData);
      setPriceInfo(priceResult);
      console.log('Price calculated:', priceResult);
    } catch (error) {
      console.error('Price calculation failed:', error);
      setError('Не удалось рассчитать стоимость поездки');
    }
  };

  // Поиск ближайших водителей
  const findNearbyDrivers = async () => {
    try {
      console.log('Finding nearby drivers:', pickupLocation.lat, pickupLocation.lng);
      const drivers = await apiService.findNearbyDrivers(
        pickupLocation.lat, 
        pickupLocation.lng, 
        3 // радиус 3 км
      );
      setNearbyDrivers(drivers);
      console.log('Nearby drivers found:', drivers);
    } catch (error) {
      console.error('Driver search failed:', error);
      // Не показываем ошибку, так как это не критично
    }
  };

  // Создание поездки
  const createRide = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      // Генерируем mock user_id (в реальном приложении будет из контекста)
      const userId = 'user_' + Date.now();
      
      const rideData = {
        user_id: userId,
        vendor_id: 1,
        pickup_datetime: new Date().toISOString(),
        dropoff_datetime: new Date(Date.now() + 20 * 60000).toISOString(), // +20 минут
        passenger_count: 1,
        pickup_latitude: pickupLocation.lat,
        pickup_longitude: pickupLocation.lng,
        dropoff_latitude: dropoffLocation.lat,
        dropoff_longitude: dropoffLocation.lng,
        trip_duration: 1200, // 20 минут в секундах
        pickup_district: 'Manhattan',
        pickup_neighbourhood: 'Midtown',
        dropoff_district: 'Brooklyn',
        dropoff_neighbourhood: 'Williamsburg',
        pickup_hour: new Date().getHours(),
        day_name: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][new Date().getDay()],
        weekday_or_weekend: new Date().getDay() >= 1 && new Date().getDay() <= 5 ? 'weekday' : 'weekend',
        month: new Date().getMonth() + 1,
        year: new Date().getFullYear(),
        season: 'Winter'
      };
      
      console.log('Creating ride:', rideData);
      const rideResult = await apiService.createRide(rideData);
      console.log('Ride created:', rideResult);
      
      // Переход к отслеживанию поездки
      navigate('/tracking');
      
    } catch (error) {
      console.error('Ride creation failed:', error);
      setError(error.message || 'Не удалось создать поездку');
    } finally {
      setIsLoading(false);
    }
  };

  // Обработка отправки формы
  const handleSubmit = async (e) => {
    e.preventDefault();
    await createRide();
  };

  // Автоматический расчет цены и поиск водителей при изменении координат
  useEffect(() => {
    if (pickupLocation.lat && dropoffLocation.lat) {
      calculatePrice();
      findNearbyDrivers();
    }
  }, [pickupLocation.lat, dropoffLocation.lat]);

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">🚖 Заказ поездки</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Форма заказа */}
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
            
            {/* Информация о маршруте */}
            <div className="bg-blue-50 p-3 rounded-md">
              <div className="text-sm text-blue-800">
                <div>📍 Отправление: {pickupLocation.lat.toFixed(6)}, {pickupLocation.lng.toFixed(6)}</div>
                <div>🏁 Назначение: {dropoffLocation.lat.toFixed(6)}, {dropoffLocation.lng.toFixed(6)}</div>
              </div>
            </div>
            
            {/* Расчет стоимости */}
            {priceInfo && (
              <div className="bg-green-50 p-3 rounded-md">
                <h3 className="font-semibold text-green-800 mb-2">💰 Стоимость поездки</h3>
                <div className="text-sm text-green-700 space-y-1">
                  <div>Базовый тариф: ${priceInfo.base_fare}</div>
                  <div>За расстояние: ${priceInfo.distance_fare}</div>
                  <div>За время: ${priceInfo.time_fare}</div>
                  {priceInfo.surge_multiplier > 1 && (
                    <div>Пиковая нагрузка: x{priceInfo.surge_multiplier}</div>
                  )}
                  <div className="font-bold text-lg">Итого: ${priceInfo.total_amount} {priceInfo.currency}</div>
                </div>
              </div>
            )}
            
            {/* Ближайшие водители */}
            {nearbyDrivers.length > 0 && (
              <div className="bg-yellow-50 p-3 rounded-md">
                <h3 className="font-semibold text-yellow-800 mb-2">🚕 Доступные водители</h3>
                <div className="text-sm text-yellow-700">
                  Найдено водителей поблизости: {nearbyDrivers.length}
                </div>
              </div>
            )}
            
            <div className="pt-4">
              <button
                type="submit"
                disabled={isLoading || !priceInfo}
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
                  priceInfo ? `Заказать поездку за $${priceInfo.total_amount}` : 'Рассчитываем стоимость...'
                )}
              </button>
            </div>
          </form>
        </div>
        
        {/* Карта */}
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
