import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import PrivateChat from './components/Chat/PrivateChat';
import GroupChat from './components/Chat/GroupChat';
import TermsAndConditions from './components/TermsAndConditions';
import Dashboard from './components/Chat/Dashboard';
import './styles.css';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/private-chat" element={<PrivateChat />} />
          <Route path="/group-chat" element={<GroupChat />} />
          <Route path="/terms-and-conditions" element={<TermsAndConditions />} />
          <Route path="/dashboard" element={<Dashboard />} />
          {/* Add more routes as needed */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
