// src/components/Home.js

import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  // Add your login logic here

  return (
    <section className="bg-gray-50 dark:bg-gray-900">
      <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
        <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
          <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
            <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white text-center">
              Welcome to CatChat
            </h1>
            {/* Buttons for Register and Login */}
          <div className="flex justify-center space-x-4">
            <Link to="/register" className="bg-blue-500 text-white px-4 py-2 rounded-md">
              Register
            </Link>
            <Link to="/login" className="bg-green-500 text-white px-4 py-2 rounded-md">
              Login
            </Link>
          </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Home;
