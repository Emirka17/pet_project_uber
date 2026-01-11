import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from 'react-router-dom';
import OrderPage from './pages/OrderPage';

// Главная страница
function Home() {
  return (
    <div className="text-center">
      <h2 className="text-3xl font-bold text-gray-800 mb-4">🏠 Главная страница</h2>
      <p className="text-gray-600 mb-8">Добро пожаловать в Uber Clone!</p>
      <Link to="/order" className="button-primary inline-block">
        Заказать поездку
      </Link>
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

// Страница отслеживания (заглушка)
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
