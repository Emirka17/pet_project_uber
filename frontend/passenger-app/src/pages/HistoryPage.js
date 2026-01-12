// Страница истории поездок
import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

function HistoryPage() {
  const [rides, setRides] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, completed, cancelled

  // Mock данные поездок
  const mockRides = [
    {
      id: 'ride_001',
      status: 'completed',
      pickup_address: 'Times Square, Manhattan',
      dropoff_address: 'Central Park, Manhattan',
      pickup_datetime: '2024-01-15T14:30:00Z',
      dropoff_datetime: '2024-01-15T14:50:00Z',
      total_fare: 15.50,
      distance_km: 2.3,
      driver: {
        name: 'Алексей Петров',
        car_model: 'Toyota Camry',
        rating: 4.8
      }
    },
    {
      id: 'ride_002',
      status: 'completed',
      pickup_address: 'Brooklyn Bridge, Brooklyn',
      dropoff_address: 'Wall Street, Manhattan',
      pickup_datetime: '2024-01-14T18:15:00Z',
      dropoff_datetime: '2024-01-14T18:35:00Z',
      total_fare: 12.75,
      distance_km: 1.8,
      driver: {
        name: 'Михаил Сидоров',
        car_model: 'Honda Civic',
        rating: 4.9
      }
    },
    {
      id: 'ride_003',
      status: 'cancelled',
      pickup_address: 'Grand Central, Manhattan',
      dropoff_address: 'Metropolitan Museum, Manhattan',
      pickup_datetime: '2024-01-13T12:00:00Z',
      dropoff_datetime: null,
      total_fare: 0,
      distance_km: 0,
      driver: null
    },
    {
      id: 'ride_004',
      status: 'completed',
      pickup_address: 'JFK Airport, Queens',
      dropoff_address: 'Midtown, Manhattan',
      pickup_datetime: '2024-01-12T09:30:00Z',
      dropoff_datetime: '2024-01-12T10:15:00Z',
      total_fare: 45.00,
      distance_km: 18.5,
      driver: {
        name: 'Дмитрий Козлов',
        car_model: 'Mercedes E-Class',
        rating: 5.0
      }
    }
  ];

  useEffect(() => {
    // Симуляция загрузки данных
    const timer = setTimeout(() => {
      setRides(mockRides);
      setLoading(false);
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed': return 'Завершена';
      case 'cancelled': return 'Отменена';
      case 'pending': return 'В ожидании';
      default: return 'Неизвестно';
    }
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return format(date, 'dd MMM yyyy, HH:mm', { locale: ru });
  };

  const filteredRides = filter === 'all' 
    ? rides 
    : rides.filter(ride => ride.status === filter);

  const totalSpent = rides
    .filter(ride => ride.status === 'completed')
    .reduce((sum, ride) => sum + ride.total_fare, 0);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">📜 История поездок</h1>
        <div className="card">
          <div className="flex items-center justify-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3">Загрузка истории...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">📜 История поездок</h1>
        <div className="mt-4 sm:mt-0">
          <span className="text-lg font-semibold">
            Всего потрачено: <span className="text-green-600">${totalSpent.toFixed(2)}</span>
          </span>
        </div>
      </div>

      {/* Фильтры */}
      <div className="card mb-6">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              filter === 'all' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Все поездки
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              filter === 'completed' 
                ? 'bg-green-600 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Завершенные
          </button>
          <button
            onClick={() => setFilter('cancelled')}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              filter === 'cancelled' 
                ? 'bg-red-600 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Отмененные
          </button>
        </div>
      </div>

      {/* Список поездок */}
      {filteredRides.length === 0 ? (
        <div className="card text-center py-12">
          <div className="text-5xl mb-4">🚕</div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">Нет поездок</h3>
          <p className="text-gray-500">
            {filter === 'all' 
              ? 'У вас пока нет поездок. Закажите первую!' 
              : `У вас нет ${filter === 'completed' ? 'завершенных' : 'отмененных'} поездок.`
            }
          </p>
          <button className="button-primary mt-4 inline-block">
            Заказать поездку
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredRides.map((ride) => (
            <div key={ride.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex flex-col sm:flex-row justify-between">
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center">
                      <span className="font-semibold">Поездка #{ride.id.slice(5)}</span>
                      <span className={`ml-3 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(ride.status)}`}>
                        {getStatusText(ride.status)}
                      </span>
                    </div>
                    {ride.total_fare > 0 && (
                      <div className="text-lg font-bold text-green-600">
                        ${ride.total_fare.toFixed(2)}
                      </div>
                    )}
                  </div>

                  <div className="space-y-2 text-sm text-gray-600">
                    <div className="flex items-start">
                      <span className="mr-2">📍</span>
                      <span>{ride.pickup_address}</span>
                    </div>
                    <div className="flex items-start">
                      <span className="mr-2">🏁</span>
                      <span>{ride.dropoff_address}</span>
                    </div>
                    
                    <div className="flex flex-wrap gap-4 mt-2">
                      <div>
                        <span className="text-gray-500">Дата:</span>
                        <span className="ml-1">{formatDateTime(ride.pickup_datetime)}</span>
                      </div>
                      {ride.distance_km > 0 && (
                        <div>
                          <span className="text-gray-500">Расстояние:</span>
                          <span className="ml-1">{ride.distance_km} км</span>
                        </div>
                      )}
                    </div>

                    {ride.driver && (
                      <div className="mt-2 pt-2 border-t border-gray-100">
                        <div className="flex items-center text-xs">
                          <span className="mr-2">👨‍✈️</span>
                          <span>{ride.driver.name}</span>
                          <span className="mx-2">•</span>
                          <span>{ride.driver.car_model}</span>
                          <span className="mx-2">•</span>
                          <span>⭐ {ride.driver.rating}</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default HistoryPage;
