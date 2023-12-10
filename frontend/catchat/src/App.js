import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import TermsAndConditions from './components/TermsAndConditions';
import Dashboard from './components/Chat/Dashboard';
import './styles.css';

/**
 * App component that handles routing
 * @returns {Element} JSX
 */
function App() {
  // JSX to render based on route
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/terms-and-conditions" element={<TermsAndConditions />} />
          <Route path="/dashboard" element={<Dashboard />} />
          {/* Add more routes as needed */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
