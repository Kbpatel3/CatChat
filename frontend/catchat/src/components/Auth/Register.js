import React from "react";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import io from "socket.io-client";

const socket = io("http://localhost:5000");

/**
 * Register component for the registration page
 * @returns {Element} JSX
 */
const Register = () => {
  // Use the navigate hook to redirect the user to the dashboard
  const navigate = useNavigate();
  // State variables for the form fields
  const [email, setEmail] = useState("");
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [terms, setTerms] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  /**
   * Handles the create account button click (Async)
   * @param event The event object
   * @returns {Promise<void>} Nothing
   */
  const handleCreateAccount = async (event) => {
    console.log("Handling create account...");
    // Prevent the default form submission behavior
    event.preventDefault();

    // Try to register the user
    try {
      // Check to see if all fields are filled out
      if (!email || !password || !confirmPassword || !userId) {
        setErrorMessage("Please fill out all fields");
        return;
      }

      // Check to see if the user accepted the terms and conditions
      if (!terms) {
        setErrorMessage("Please accept the terms and conditions");
        return;
      }

      // Check if email is valid (contains @)
      if (!email.includes("@")) {
        setErrorMessage("Please enter a valid email");
        return;
      }

      // Check if passwords match
      if (password !== confirmPassword) {
        setErrorMessage("Passwords do not match");
        return;
      }

      // Send the registration request to the server passing in the email, userId, and password
      socket.emit("register", { email, userId, password });

      // Wait for the server to respond with the success or failure message (Front end calls back end's register_response event)
      socket.on("register_response", (data) => {
        console.log("Received register response from server")
        // If the success property is true, then the registration was successful
        if (data.success) {
          console.log(data.message);
          // Clear the error message
          setErrorMessage('');
          // Navigate to the dashboard passing in the userId as state
          navigate('/dashboard' , { state: { userId: userId } });
        } else {
          console.error(data.message);
          // Set the error message because the registration failed and the backend sent back a failure message
          setErrorMessage(data.message);
        }
        });
    } catch (error) {
      console.error('Error during registration:', error);
      // Set the error message because the registration failed and the backend threw an error
      setErrorMessage('Error during registration');
    }
  };

  /**
   * Simple function to route the user to the login page
   */
  const routeLogin = () => {
    // Use the navigate hook to redirect the user to the login page
    navigate("/login");
  };

  return (
    <div>
      <section className="bg-gray-50 dark:bg-gray-900">
        <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
          <div className="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700">
            <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
              <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
                Create and account
              </h1>
              <form className="space-y-4 md:space-y-6" action="#">
              {errorMessage && (
                  <div className="bg-red-500 text-white p-3 mb-4 rounded-md">
                    {errorMessage}
                  </div>
                )}
                <div>
                  <label
                    htmlFor="email"
                    className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Your email
                  </label>
                  <input
                    type="email"
                    name="email"
                    id="email"
                    className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="name@company.com"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    required=""></input>
                </div>
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
                    placeholder="Username"
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
                <div>
                  <label
                    htmlFor="confirm-password"
                    className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Confirm password
                  </label>
                  <input
                    type="password"
                    name="confirm-password"
                    id="confirm-password"
                    placeholder="••••••••"
                    className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    value={confirmPassword}
                    onChange={(event) => setConfirmPassword(event.target.value)}
                    required=""></input>
                </div>
                <div className="flex items-start">
                  <div className="flex items-center h-5">
                    <input
                      id="terms"
                      aria-describedby="terms"
                      type="checkbox"
                      value={terms}
                      onChange={(event) => setTerms(event.target.checked)}
                      className="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800"
                      required=""></input>
                  </div>
                  <div className="ml-3 text-sm">
                    <label
                      htmlFor="terms"
                      className="font-light text-gray-500 dark:text-gray-300">
                      I accept the{" "}
                      <a
                        className="font-medium text-primary-600 hover:underline dark:text-primary-500"
                        href="/terms-and-conditions">
                        Terms and Conditions
                      </a>
                    </label>
                  </div>
                </div>
                <button
                  type="submit"
                  className="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800 border"
                  onClick={handleCreateAccount}>
                  Create an account
                </button>
                <p className="text-sm font-light text-gray-500 dark:text-gray-400">
                  Already have an account?{" "}
                  <button
                    type="submit"
                    className="font-medium text-primary-600 hover:underline dark:text-primary-500"
                    onClick={routeLogin}>
                    Login
                  </button>
                </p>
              </form>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Register;
