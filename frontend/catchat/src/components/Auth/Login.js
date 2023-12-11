// src/components/Auth/Login.js

import React from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import io from "socket.io-client";

const socket = io("http://localhost:5000");

/**
 * Login page component
 * @returns {Element} JSX
 */
const Login = () => {
  // Use the navigate hook to redirect the user to the dashboard after login
  const navigate = useNavigate();

  // State variables for the login form
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  /**
   * Handle the login form submission (Async)
   * @param event The form submission event
   * @returns {Promise<void>} Nothing
   */
  const handleLogin = async (event) => {
    //console.log("Login button clicked");
    // Prevent the default form submission behavior
    event.preventDefault();

    // Try to log in
    try {
      // Check to see if all fields are filled out
        if (!userId || !password) {
            setErrorMessage("Please fill out all fields");
            return;
        }

        // Send the login request to the server passing in the user's credentials (userId and password)
      socket.emit("login", { userId, password });

      // Wait for the server to respond with the login_response event (success or failure)
      socket.once("login_response", (data) => {
        // If the login was successful, redirect the user to the dashboard
        if (data.success) {
          console.log(data.message);
          // Clear the error message
          setErrorMessage("");
          // Redirect the user to the dashboard and pass in the userId as state
          navigate("/dashboard", { state: { userId: userId } });
        } else {
          // If the login was not successful, display the error message
          console.log(data.message);
          setErrorMessage(data.message);
        }
      });
    } catch (error) {
        // If there was an error, log it to the console and display the error message
      console.error("Error during login: ", error);
      setErrorMessage("Error during login. Please try again.");
    }
  };

  /**
   * Route the user to the register page
   */
  const routeRegister = () => {
    navigate("/register");
  };

  return (
    <section className="bg-gray-50 dark:bg-gray-900">
      <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
        <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
          <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
            <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
              Sign in to your account
            </h1>
            <form className="space-y-4 md:space-y-6" onSubmit={handleLogin}>
              {errorMessage && (
                <div className="bg-red-500 text-white p-3 mb-4 rounded-md">
                  {errorMessage}
                </div>
              )}
              <div>
                <label
                  htmlFor="userId"
                  className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                  Your Username
                </label>
                <input
                  type="text"
                  name="userId"
                  id="userId"
                  className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder="name@company.com"
                  value={userId}
                  onChange={(event) => setUserId(event.target.value)}
                  required=""></input>
              </div>
              <div>
                <label
                  htmlFor="password"
                  className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                  Password
                </label>
                <input
                  type="password"
                  name="password"
                  id="password"
                  placeholder="••••••••"
                  className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required=""></input>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-start">
                  <div className="flex items-center h-5">
                    <input
                      id="remember"
                      aria-describedby="remember"
                      type="checkbox"
                      className="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800"
                      required=""></input>
                  </div>
                  <div className="ml-3 text-sm">
                    <label
                      htmlFor="remember"
                      className="text-gray-500 dark:text-gray-300">
                      Remember me
                    </label>
                  </div>
                </div>
                <a
                  href="#"
                  className="block text-sm font-medium text-gray-900 dark:text-white">
                  Forgot password?
                </a>
              </div>
              <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                Don't have an account?{" "}
                <button
                  type="submit"
                  className="font-medium text-primary-600 hover:underline dark:text-primary-500"
                  onClick={routeRegister}>
                  Register
                </button>
              </p>
              <button
                type="submit"
                className="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800 border">
                Login to account
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Login;
