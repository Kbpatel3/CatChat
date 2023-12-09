import React, { useEffect, useState } from "react";
import { eventEmitter } from "../../events/EventEmitter";
import io from "socket.io-client";

// Create a socket connection to the server
const socket = io("http://localhost:5000");

/**
 * MessageList component that renders a list of messages between two users in a chat
 * @param sender The username of the user who is logged in
 * @returns {Element} JSX
 */
function MessageList({ sender }) {
  // State to store the messages
  const [messages, setMessages] = useState([]);

  // State to store the user id of the user that the logged in user is chatting with
  const[userId, setUserId] = useState("");

  // On every render, do the following
  useEffect(() => {

    /**
     * Handle a card being clicked. This is a callback function that is called when the 'cardClick' event is emitted
     * @param userId The user id of the user that the logged in user is chatting with
     */
    const handleCardClicked = (userId) => {
      // Set the user id state to the input value
      setUserId(userId)

      // Clear the messages state
      setMessages([])
      console.log("Starting chat with " + userId);
      console.log("From " + sender);
      // Get the message history between the logged in user and the user that they are chatting with
      getMessageHistory(sender, userId);
    };

    /**
     * Callback function that is called when the 'cardClicked' event is emitted
     * @param userId The user id of the user that the logged in user is chatting with
     */
    const cardClickListener = (userId) => {
      // Call the handleCardClicked function
      handleCardClicked(userId);
    };

    /**
     * Callback function that is called when the 'messageSent' event is emitted
     * @param message The message that was sent
     */
    const messageListener = (message) => {
        // Send the message to the server via the socket connection passing in the sender, message, and userId
        socket.emit("newMessage", { sender, message, userId });
    }

    // Listen to the event emitter for a card being clicked and a message being sent
    eventEmitter.on("cardClicked", cardClickListener);
    eventEmitter.on('messageSent', messageListener);

  }, [sender, userId]);

  /**
   * Get the message history between the logged in user and the user that they are chatting with from the server
   * @param sender The username of the user who is logged in
   * @param receiver The username of the user that the logged in user is chatting with
   */
  const getMessageHistory = (sender, receiver) => {
    console.log("Getting message history between " + sender + " and " + receiver);

    // Send the server a request for the message history between the logged in user and the user that they are chatting with
    socket.emit("getMessageHistory", { sender, receiver });

    // Listen to the socket for the message history
    socket.once("messageHistory", (data) => {
      console.log("Received message history");
      console.log(data);

      // Set the message state to the input value
      setMessages(data.messages);
    });
  };

  return (
      <div className="flex items-center justify-center h-full">
        <div className="p-4">
          {messages.length > 0 ? (
            <ul>
              {messages.map((message, index) => (
                <li key={index}>From: {message.from_user_id} - {message.message}</li>
              ))}
            </ul>
          ) : (
            <p className={"font-bold"}>Click on a chat to load messages</p>
          )}
        </div>
      </div>
    );


}

export default MessageList;
