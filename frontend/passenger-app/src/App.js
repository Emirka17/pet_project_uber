import React, { useState } from 'react'; // Добавил useState
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useNavigate // Добавил useNavigate
} from 'react-router-dom';
import OrderPage from './pages/OrderPage';
import apiService from './services/api';

// Главная страница
function Home() {
  return (
    <div className="text-center">
      <h2 className="text-3xl font-bold text-gray-800 mb-4">🏠 Добро пожаловать в Uber Clone!</h2>
      <p className="text-gray-600 mb-8">Закажите поездку быстро и удобно</p>
      
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <Link to="/order" className="button-primary inline-block">
          Заказать поездку
        </Link>
        <Link to="/login" className="button-secondary inline-block">
          Войти
        </Link>
        <Link to="/register" className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition duration-200 inline-block">
          Регистрация
        </Link>
      </div>
    </div>
  );
}

// Страница регистрации
// Страница регистрации с реальной интеграцией
function RegisterPage() {
  const [formData, setFormData] = useState({
    phone: '',
    first_name: '',
    last_name: '',
    email: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
// ddd@example.com
    try {
      console.log('Register attempt:', formData);

      const fullName = (formData.first_name + ' ' +formData.last_name).trim(); // Объединяем имя и фамилию
      
      // Преобразуем данные для User Service
      const userData = {
        phone: formData.phone,
        name: fullName,
        email: formData.email
      };

      console.log('Sending user data:', userData)
      
      // Отправляем данные в User Service
      const response = await apiService.register(userData);
      console.log('Registration successful:', response);
      
      // Переходим на страницу логина
      navigate('/login');
    } catch (err) {
      console.error('Registration failed:', err);
      setError(err.message || 'Ошибка регистрации');
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="max-w-md mx-auto card">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">הרשמה</h2>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Телефон
          </label>
          <input
            type="tel"
            value={formData.phone}
            onChange={(e) => setFormData({...formData, phone: e.target.value})}
            placeholder="+7 (999) 123-45-67"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Имя
            </label>
            <input
              type="text"
              value={formData.first_name}
              onChange={(e) => setFormData({...formData, first_name: e.target.value})}
              placeholder="Иван"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Фамилия
            </label>
            <input
              type="text"
              value={formData.last_name}
              onChange={(e) => setFormData({...formData, last_name: e.target.value})}
              placeholder="Иванов"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Email
          </label>
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            placeholder="ivan@example.com"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full button-primary"
        >
          {loading ? 'Регистрация...' : 'Зарегистрироваться'}
        </button>
      </form>
      
      <div className="mt-4 text-center">
        <Link to="/login" className="text-blue-600 hover:text-blue-800">
          Уже есть аккаунт? Войти
        </Link>
      </div>
    </div>
  );
}


// Страница логина
function LoginPage() {
  const [formData, setFormData] = useState({
    phone: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      console.log('Login:', formData);
      // Здесь будет вызов API
      await new Promise(resolve => setTimeout(resolve, 1000)); // Mock
      navigate('/order');
    } catch (err) {
      setError(err.message || 'Ошибка входа');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto card">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">כניסה</h2>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Телефон
          </label>
          <input
            type="tel"
            value={formData.phone}
            onChange={(e) => setFormData({...formData, phone: e.target.value})}
            placeholder="+7 (999) 123-45-67"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Пароль
          </label>
          <input
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            placeholder="••••••••"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full button-primary"
        >
          {loading ? 'Вход...' : 'Войти'}
        </button>
      </form>
      
      <div className="mt-4 text-center">
        <Link to="/register" className="text-blue-600 hover:text-blue-800">
          Нет аккаунта? Регистрация
        </Link>
      </div>
    </div>
  );
}

// История поездок
function History() {
  return (
    <div className="text-center">
      <h2 className="text-3xl font-bold text-gray-800 mb-4">📜 История поездок</h2>
      <p className="text-gray-600">Здесь будет список ваших поездок</p>
    </div>
  );
}

// Профиль
function Profile() {
  return (
    <div className="text-center">
      <h2 className="text-3xl font-bold text-gray-800 mb-4">👤 Профиль</h2>
      <p className="text-gray-600">Информация о вашем профиле</p>
    </div>
  );
}

// Страница отслеживания
function Tracking() {
  return (
    <div className="text-center">
      <h2 className="text-3xl font-bold text-gray-800 mb-4">📍 Отслеживание поездки</h2>
      <p className="text-gray-600">Ваша поездка в процессе...</p>
      <div className="mt-6">
        <div className="inline-block bg-green-100 text-green-800 px-4 py-2 rounded-full">
          Водитель найден
        </div>
      </div>
    </div>
  );
}

// 404 страница
function NotFound() {
  return (
    <div className="text-center">
      <h2 className="text-3xl font-bold text-red-600 mb-4">❌ Страница не найдена</h2>
      <Link to="/" className="text-blue-600 hover:text-blue-800">
        Вернуться на главную
      </Link>
    </div>
  );
}

// Основной компонент
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Шапка */}
        <header className="header">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-blue-600">🚗 Uber Clone</h1>
              <nav>
                <ul className="flex space-x-6">
                  <li>
                    <Link to="/" className="text-gray-700 hover:text-blue-600 transition-colors">
                      Главная
                    </Link>
                  </li>
                  <li>
                    <Link to="/history" className="text-gray-700 hover:text-blue-600 transition-colors">
                      История
                    </Link>
                  </li>
                  <li>
                    <Link to="/profile" className="text-gray-700 hover:text-blue-600 transition-colors">
                      Профиль
                    </Link>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </header>

        {/* Основной контент */}
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/order" element={<OrderPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/history" element={<History />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/tracking" element={<Tracking />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>

        {/* Футер */}
        <footer className="bg-white border-t mt-12">
          <div className="container mx-auto px-4 py-6">
            <p className="text-center text-gray-500">
              © 2024 Uber Clone - Pet Project
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
