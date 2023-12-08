import React, { useEffect, useState } from "react";
import { eventEmitter } from "../../events/EventEmitter";
import io from "socket.io-client";

const socket = io("http://localhost:5000");

function MessageList({ sender }) {
  const [messages, setMessages] = useState([]);
  const[userId, setUserId] = useState("");

  useEffect(() => {
    const handleCardClicked = (userId) => {
      setUserId(userId)
      setMessages([])
      console.log("Starting chat with " + userId);
      console.log("From " + sender);
      getMessageHistory(sender, userId);
    };

    // Subscribe to the 'cardClick' event
    const cardClickListener = (userId) => {
      handleCardClicked(userId);
    };

    const messageListener = (message) => {
        socket.emit("newMessage", { sender, message, userId });
    }

    eventEmitter.on("cardClicked", cardClickListener);
    eventEmitter.on('messageSent', messageListener);

  }, [sender, userId]);

  const getMessageHistory = (sender, receiver) => {
    console.log("Getting message history between " + sender + " and " + receiver);
    socket.emit("getMessageHistory", { sender, receiver });

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
