// Страница отслеживания поездки
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import MapComponent from '../components/MapComponent';

function TrackingPage() {
  const navigate = useNavigate();
  
  // Mock данные поездки (в реальном приложении будут из контекста/стейта)
  const [ride, setRide] = useState({
    id: 'ride_' + Date.now(),
    status: 'pending',
    pickup_location: { lat: 40.7128, lng: -74.0060, address: 'Times Square, New York' },
    dropoff_location: { lat: 40.7580, lng: -73.9855, address: 'Central Park, New York' },
    driver: {
      id: 'driver_123',
      name: 'Михаил Петров',
      car_model: 'Toyota Camry',
      car_plate: 'A123BC',
      phone: '+1234567890',
      rating: 4.8
    },
    price: 15.50,
    estimated_arrival: '5 мин'
  });

  const [driverLocation, setDriverLocation] = useState({
    lat: 40.7200,
    lng: -74.0100
  });

  // Симуляция изменения статуса поездки
  useEffect(() => {
    const statusTimer = setTimeout(() => {
      setRide(prev => ({
        ...prev,
        status: 'driver_assigned',
        estimated_arrival: '3 мин'
      }));
    }, 3000);

    const arrivalTimer = setTimeout(() => {
      setRide(prev => ({
        ...prev,
        status: 'driver_arrived',
        estimated_arrival: '0 мин'
      }));
    }, 8000);

    const startTimer = setTimeout(() => {
      setRide(prev => ({
        ...prev,
        status: 'in_progress'
      }));
    }, 12000);

    const completeTimer = setTimeout(() => {
      setRide(prev => ({
        ...prev,
        status: 'completed'
      }));
    }, 20000);

    return () => {
      clearTimeout(statusTimer);
      clearTimeout(arrivalTimer);
      clearTimeout(startTimer);
      clearTimeout(completeTimer);
    };
  }, []);

  // Симуляция движения водителя
  useEffect(() => {
    if (ride.status === 'driver_assigned' || ride.status === 'driver_arrived') {
      const moveInterval = setInterval(() => {
        setDriverLocation(prev => ({
          lat: prev.lat + (Math.random() - 0.5) * 0.001,
          lng: prev.lng + (Math.random() - 0.5) * 0.001
        }));
      }, 2000);

      return () => clearInterval(moveInterval);
    }
  }, [ride.status]);

  const handleCompleteRide = () => {
    // Переход к оплате или завершению
    navigate('/payment');
  };

  const getStatusInfo = () => {
    switch (ride.status) {
      case 'pending':
        return { text: 'Поиск водителя...', color: 'bg-yellow-500', message: 'Ищем ближайшего водителя' };
      case 'driver_assigned':
        return { text: 'Водитель найден', color: 'bg-blue-500', message: 'Водитель в пути к вам' };
      case 'driver_arrived':
        return { text: 'Водитель прибыл', color: 'bg-green-500', message: 'Водитель ждет вас' };
      case 'in_progress':
        return { text: 'Поездка', color: 'bg-purple-500', message: 'Поездка в процессе' };
      case 'completed':
        return { text: 'Завершено', color: 'bg-gray-500', message: 'Поездка завершена' };
      default:
        return { text: 'Неизвестно', color: 'bg-gray-300', message: 'Статус неизвестен' };
    }
  };

  const statusInfo = getStatusInfo();

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">📍 Отслеживание поездки</h1>
      
      {/* Статус поездки */}
      <div className="card mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold">Поездка #{ride.id.slice(0, 8)}</h2>
            <p className="text-gray-600">{statusInfo.message}</p>
          </div>
          <div className={`px-4 py-2 rounded-full text-white font-medium ${statusInfo.color}`}>
            {statusInfo.text}
          </div>
        </div>
        
        {ride.status !== 'completed' && (
          <div className="mt-4 p-3 bg-blue-50 rounded-md">
            <div className="flex items-center justify-between">
              <span className="text-blue-800 font-medium">
                ⏰ Прибытие через: {ride.estimated_arrival}
              </span>
              {ride.driver && (
                <span className="text-blue-800">
                  🚕 {ride.driver.name} • {ride.driver.car_model}
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Информация о водителе */}
        {ride.driver && ride.status !== 'completed' && (
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">👨‍✈️ Информация о водителе</h3>
            <div className="space-y-3">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-gray-300 rounded-full flex items-center justify-center mr-3">
                  <span className="text-xl">👤</span>
                </div>
                <div>
                  <div className="font-medium">{ride.driver.name}</div>
                  <div className="text-sm text-gray-600">Рейтинг: ⭐ {ride.driver.rating}</div>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4 pt-2">
                <div>
                  <div className="text-sm text-gray-600">Автомобиль</div>
                  <div className="font-medium">{ride.driver.car_model}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Номер</div>
                  <div className="font-medium">{ride.driver.car_plate}</div>
                </div>
              </div>
              
              <button className="w-full button-secondary mt-4">
                📞 Позвонить водителю
              </button>
            </div>
          </div>
        )}

        {/* Стоимость и действия */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">💰 Стоимость поездки</h3>
          <div className="text-3xl font-bold text-center mb-4">
            ${ride.price}
          </div>
          
          {ride.status === 'completed' ? (
            <div className="space-y-3">
              <button 
                onClick={handleCompleteRide}
                className="w-full button-primary"
              >
                Перейти к оплате
              </button>
              <button 
                onClick={() => navigate('/order')}
                className="w-full button-secondary"
              >
                Заказать еще одну поездку
              </button>
            </div>
          ) : (
            <div className="text-center text-gray-600">
              <p>Оплата будет доступна после завершения поездки</p>
            </div>
          )}
        </div>
      </div>

      {/* Карта */}
      <div className="card mt-8">
        <h3 className="text-lg font-semibold mb-4">🗺️ Маршрут поездки</h3>
        <MapComponent 
          pickupLocation={ride.pickup_location}
          dropoffLocation={ride.dropoff_location}
          driverLocation={driverLocation}
          onMapClick={null}
        />
      </div>
    </div>
  );
}

export default TrackingPage;
