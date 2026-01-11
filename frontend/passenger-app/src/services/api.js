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
      console.log('API Request:', url, config);
      const response = await fetch(url, config);
      
      console.log('API Response:', response.status, response.statusText);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('API Error:', errorData);
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
    console.log('Register user:', userData);
    return this.request('/api/v1/users/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async getCurrentUser(phone) {
    console.log('Get current user by phone:', phone);
    return this.request(`/api/v1/users/me?phone=${encodeURIComponent(phone)}`);
  }

  async getUser(userId) {
    return this.request(`/api/v1/users/${userId}`);
  }

  // Ride Service методы
  async createRide(rideData) {
    console.log('Create ride:', rideData);
    return this.request('/api/v1/rides/', {
      method: 'POST',
      body: JSON.stringify(rideData),
    });
  }

  async getRideHistory() {
    // Пока mock
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
    console.log('Calculate price:', pricingData);
    return this.request('/api/v1/pricing/calculate', {
      method: 'POST',
      body: JSON.stringify(pricingData),
    });
  }

  // Payment Service методы
  async processPayment(paymentData) {
    console.log('Process payment:', paymentData);
    return this.request('/api/v1/payments/process', {
      method: 'POST',
      body: JSON.stringify(paymentData),
    });
  }

  // Geo Service методы
  async findNearbyDrivers(lat, lon, radius = 3) {
    console.log('Find nearby drivers:', lat, lon, radius);
    return this.request(`/api/v1/geo/drivers/nearby?lat=${lat}&lon=${lon}&radius_km=${radius}`);
  }
}

// Экспортируем singleton инстанс
const apiService = new ApiService();
export default apiService;
