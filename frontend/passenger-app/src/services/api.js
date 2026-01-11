// API service для взаимодействия с backend сервисами

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('token');
  }

  // Установка токена авторизации
  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }

  // Базовый метод для HTTP запросов
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(this.token && { 'Authorization': `Bearer ${this.token}` }),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // User Service методы
  async register(userData) {
    return this.request('/api/v1/users/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async getCurrentUser(phone) {
    // Сначала попробуем получить пользователя по phone
    try {
      return await this.request(`/api/v1/users/me?phone=${encodeURIComponent(phone)}`);
    } catch (error) {
      console.log('User not found by phone, creating new user...');
      // Если не найден - создаем нового
      return await this.register({
        phone: phone,
        first_name: 'User',
        last_name: 'Test',
        email: `${phone.replace('+', '')}@example.com`
      });
    }
  }

  async getUser(userId) {
    return this.request(`/api/v1/users/${userId}`);
  }

  // Ride Service методы
  async createRide(rideData) {
    return this.request('/api/v1/rides/', {
      method: 'POST',
      body: JSON.stringify(rideData),
    });
  }

  async getRideHistory() {
    // Пока mock, позже интегрируем с реальным API
    return [
      {
        id: 'ride_123',
        user_id: 'user_456',
        status: 'completed',
        pickup_district: 'Manhattan',
        dropoff_district: 'Brooklyn',
        total_fare: 15.50,
        created_at: '2024-01-15T14:30:00Z'
      }
    ];
  }

  // Pricing Service методы
  async calculatePrice(pricingData) {
    return this.request('/api/v1/pricing/calculate', {
      method: 'POST',
      body: JSON.stringify(pricingData),
    });
  }

  // Payment Service методы
  async processPayment(paymentData) {
    return this.request('/api/v1/payments/process', {
      method: 'POST',
      body: JSON.stringify(paymentData),
    });
  }
}

// Экспортируем singleton инстанс
const apiService = new ApiService();
export default apiService;
