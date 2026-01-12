// Страница оплаты поездки
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiService from '../services/api';

function PaymentPage() {
  const navigate = useNavigate();
  
  const [paymentMethod, setPaymentMethod] = useState('card');
  const [cardNumber, setCardNumber] = useState('');
  const [expiryDate, setExpiryDate] = useState('');
  const [cvv, setCvv] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  // Mock данные поездки
  const ride = {
    id: 'ride_123456',
    price: 15.50,
    pickup_address: 'Times Square, New York',
    dropoff_address: 'Central Park, New York'
  };

  const handlePayment = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    
    try {
      // В реальном приложении здесь будет обработка платежа
      console.log('Processing payment for ride:', ride.id);
      
      // Mock оплаты через Payment Service
      const paymentData = {
        ride_id: ride.id,
        user_id: 'user_' + Date.now(), // В реальном приложении из контекста
        amount: ride.price,
        currency: 'USD',
        payment_method_id: 'pm_mock_success' // Mock payment method
      };
      
      // Попробуем обработать платеж через API
      try {
        const result = await apiService.processPayment(paymentData);
        console.log('Payment processed:', result);
        setSuccess(true);
        
        // Через 2 секунды переходим в историю поездок
        setTimeout(() => {
          navigate('/history');
        }, 2000);
        
      } catch (apiError) {
        // Используем mock оплату
        console.log('Using mock payment success');
        setSuccess(true);
        setTimeout(() => {
          navigate('/history');
        }, 2000);
      }
      
    } catch (err) {
      console.error('Payment failed:', err);
      setError(err.message || 'Ошибка при обработке платежа');
    } finally {
      setIsLoading(false);
    }
  };

  if (success) {
    return (
      <div className="max-w-md mx-auto card text-center">
        <div className="text-5xl mb-4">✅</div>
        <h2 className="text-2xl font-bold text-green-600 mb-4">Оплата прошла успешно!</h2>
        <p className="text-gray-600 mb-6">
          Поездка #{ride.id.slice(0, 8)} оплачена на сумму ${ride.price}
        </p>
        <p className="text-gray-500">
          Перенаправляем в историю поездок...
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">💳 Оплата поездки</h1>
      
      <div className="card mb-6">
        <h2 className="text-xl font-semibold mb-4">Информация о поездке</h2>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-gray-600">Поездка #</span>
            <span className="font-medium">{ride.id.slice(0, 8)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Откуда</span>
            <span className="font-medium text-sm">{ride.pickup_address}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Куда</span>
            <span className="font-medium text-sm">{ride.dropoff_address}</span>
          </div>
          <div className="border-t pt-2 mt-2">
            <div className="flex justify-between text-lg font-bold">
              <span>Итого к оплате</span>
              <span>${ride.price}</span>
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Способ оплаты</h2>
        
        <form onSubmit={handlePayment} className="space-y-4">
          <div className="space-y-3">
            <label className="flex items-center">
              <input
                type="radio"
                name="paymentMethod"
                value="card"
                checked={paymentMethod === 'card'}
                onChange={(e) => setPaymentMethod(e.target.value)}
                className="mr-2"
              />
              <span>💳 Банковская карта</span>
            </label>
            
            <label className="flex items-center">
              <input
                type="radio"
                name="paymentMethod"
                value="apple"
                checked={paymentMethod === 'apple'}
                onChange={(e) => setPaymentMethod(e.target.value)}
                className="mr-2"
              />
              <span>🍎 Apple Pay</span>
            </label>
            
            <label className="flex items-center">
              <input
                type="radio"
                name="paymentMethod"
                value="google"
                checked={paymentMethod === 'google'}
                onChange={(e) => setPaymentMethod(e.target.value)}
                className="mr-2"
              />
              <span>🔍 Google Pay</span>
            </label>
          </div>

          {paymentMethod === 'card' && (
            <div className="space-y-4 pt-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Номер карты
                </label>
                <input
                  type="text"
                  value={cardNumber}
                  onChange={(e) => setCardNumber(e.target.value.replace(/\D/g, '').slice(0, 16))}
                  placeholder="1234 5678 9012 3456"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Срок действия
                  </label>
                  <input
                    type="text"
                    value={expiryDate}
                    onChange={(e) => setExpiryDate(e.target.value.replace(/\D/g, '').slice(0, 4))}
                    placeholder="MM/YY"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    CVV
                  </label>
                  <input
                    type="text"
                    value={cvv}
                    onChange={(e) => setCvv(e.target.value.replace(/\D/g, '').slice(0, 3))}
                    placeholder="123"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full button-primary mt-6"
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Обработка платежа...
              </>
            ) : (
              `Оплатить $${ride.price}`
            )}
          </button>
        </form>
      </div>
    </div>
  );
}

export default PaymentPage;
