// Страница профиля пользователя
import React, { useState, useEffect } from 'react';
import apiService from '../services/api';

function ProfilePage() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({});
  const [stats, setStats] = useState({
    total_rides: 12,
    total_spent: 186.50,
    rating: 4.9,
    favorite_district: 'Manhattan'
  });

  // Mock данные пользователя
  const mockUser = {
    id: 'user_123456789',
    phone: '+7 (999) 123-45-67',
    name: 'Иван Иванов',
    email: 'ivan@example.com',
    rating: 4.90,
    total_rides: 12,
    created_at: '2024-01-01T10:00:00Z',
    payment_methods: [
      { id: 'pm_1', type: 'card', last4: '4242', brand: 'Visa', is_default: true },
      { id: 'pm_2', type: 'apple', name: 'Apple Pay' }
    ]
  };

  useEffect(() => {
    // Симуляция загрузки данных пользователя
    const timer = setTimeout(() => {
      setUser(mockUser);
      setFormData({
        name: mockUser.name,
        email: mockUser.email,
        phone: mockUser.phone
      });
      setLoading(false);
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  const handleSave = async () => {
    try {
      // В реальном приложении здесь будет вызов API
      console.log('Saving profile:', formData);
      
      // Имитация сохранения
      setUser({
        ...user,
        ...formData
      });
      
      setEditing(false);
    } catch (error) {
      console.error('Save failed:', error);
      alert('Ошибка при сохранении профиля');
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">👤 Профиль</h1>
        <div className="card">
          <div className="flex items-center justify-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3">Загрузка профиля...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">👤 Профиль</h1>

      {/* Основная информация */}
      <div className="card mb-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold">Основная информация</h2>
          {!editing ? (
            <button
              onClick={() => setEditing(true)}
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              Редактировать
            </button>
          ) : (
            <div className="space-x-2">
              <button
                onClick={handleSave}
                className="button-primary text-sm px-4 py-1"
              >
                Сохранить
              </button>
              <button
                onClick={() => {
                  setEditing(false);
                  setFormData({
                    name: user.name,
                    email: user.email,
                    phone: user.phone
                  });
                }}
                className="button-secondary text-sm px-4 py-1"
              >
                Отмена
              </button>
            </div>
          )}
        </div>

        <div className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Имя
              </label>
              {editing ? (
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              ) : (
                <div className="text-gray-900">{user.name}</div>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Телефон
              </label>
              {editing ? (
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              ) : (
                <div className="text-gray-900">{user.phone}</div>
              )}
            </div>

            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              {editing ? (
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              ) : (
                <div className="text-gray-900">{user.email}</div>
              )}
            </div>
          </div>

          <div className="pt-4 border-t border-gray-100">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="text-center p-3 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{stats.total_rides}</div>
                <div className="text-sm text-gray-600">Поездок</div>
              </div>
              <div className="text-center p-3 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">${stats.total_spent}</div>
                <div className="text-sm text-gray-600">Потрачено</div>
              </div>
              <div className="text-center p-3 bg-yellow-50 rounded-lg">
                <div className="text-2xl font-bold text-yellow-600">⭐ {stats.rating}</div>
                <div className="text-sm text-gray-600">Рейтинг</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Способы оплаты */}
      <div className="card mb-6">
        <h2 className="text-xl font-semibold mb-4">💳 Способы оплаты</h2>
        
        <div className="space-y-3">
          {user.payment_methods && user.payment_methods.map((method) => (
            <div key={method.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
              <div className="flex items-center">
                <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center mr-3">
                  {method.type === 'card' ? '💳' : '🍎'}
                </div>
                <div>
                  <div className="font-medium">
                    {method.type === 'card' 
                      ? `${method.brand} •••• ${method.last4}` 
                      : method.name}
                  </div>
                  {method.is_default && (
                    <div className="text-xs text-blue-600">По умолчанию</div>
                  )}
                </div>
              </div>
              <button className="text-gray-400 hover:text-gray-600">
                ⋯
              </button>
            </div>
          ))}
        </div>

        <button className="w-full mt-4 py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-gray-400 hover:text-gray-700 transition-colors">
          + Добавить способ оплаты
        </button>
      </div>

      {/* Дополнительная информация */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">ℹ️ Дополнительная информация</h2>
        
        <div className="space-y-3 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">Дата регистрации</span>
            <span>{formatDate(user.created_at)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Любимый район</span>
            <span>{stats.favorite_district}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Язык</span>
            <span>Русский</span>
          </div>
        </div>

        <div className="mt-6 pt-4 border-t border-gray-100">
          <button className="w-full py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors">
            Выйти из аккаунта
          </button>
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;
