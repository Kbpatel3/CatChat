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

  // State to store the user id of the user that the logged-in user is chatting with
  const[userId, setUserId] = useState("");

  // Reference to the end of the message list
  const messageEndRef = React.useRef(null);

  // State to see if the user is typing
    const [isTyping, setIsTyping] = useState(false);

  // On every render, do the following
  useEffect(() => {
    // Listening for our EventEmitter events
    eventEmitter.on("cardClicked", cardClickListener);
    eventEmitter.on('messageSent', messageListener);
    eventEmitter.on("typing", typingListener);
    eventEmitter.on("notTyping", notTypingListener);

    return () => {
        // Remove the event listeners
        eventEmitter.unsubscribe("cardClicked", cardClickListener);
        eventEmitter.unsubscribe('messageSent', messageListener);
        eventEmitter.unsubscribe("typing", typingListener);
        eventEmitter.unsubscribe("notTyping", notTypingListener);

        // Remove the socket listeners
        socket.off("messageHistory");
        socket.off("newMessage");
    }
  });


  // Scroll to the bottom of the message list when the messages state changes
    useEffect(() => {
      messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    // Constantly get the message history between the logged-in user and the user that they are chatting with
    useEffect(() => {
        getMessageHistory(sender, userId)
    });


  /**
  //    * Callback function that is called when the 'cardClicked' event is emitted
  //    * @param userId The user id of the user that the logged-in user is chatting with
  //    */
    const cardClickListener = (userId) => {
      // Call the handleCardClicked function
      handleCardClicked(userId);
    };

    /**
  //    * Handle a card being clicked. This is a callback function that is called when the 'cardClick' event is emitted
  //    * @param userId The user id of the user that the logged-in user is chatting with
  //    */
    const handleCardClicked = (userId) => {
      // Set the user id state to the input value
      setUserId(userId)

      // Clear the messages state
      setMessages([])
      //console.log("Starting chat with " + userId);
      //console.log("From " + sender);
      // Get the message history between the logged-in user and the user that they are chatting with
      getMessageHistory(sender, userId);
    };

    /**
  //    * Callback function that is called when the 'messageSent' event is emitted
  //    * @param message The message that was sent
  //    */
    const messageListener = (message) => {
        console.log("Message sent: " + message);
        console.log("To: " + userId);
        console.log("From: " + sender);

        // Send the message to the server via the socket connection passing in the sender, message, and userId
        socket.emit("newMessage", { sender, message, userId });

        console.log("Clearing messages")
        console.log(messages);
    }

    const typingListener = (typer) => {
        console.log(typer + " is typing...")
        console.log(sender + " is typing...")
        if (typer === sender) {
            setIsTyping(true);
        }
    }

    const notTypingListener = (typer) => {
        console.log(typer + " is not typing...")
        console.log(sender + " is not typing...")
        if (typer === sender) {
            setIsTyping(false);
        }
    }

  /**
   * Get the message history between the logged-in user and the user that they are chatting with from the server
   * @param sender The username of the user who is logged in
   * @param receiver The username of the user that the logged-in user is chatting with
   */
  const getMessageHistory = (sender, receiver) => {
    // Remove the previous listener
    socket.off("messageHistory");

    // Send the server a request for the message history between the logged-in user and the user that they are chatting with
    socket.emit("getMessageHistory", { sender, receiver });

    // Listen to the socket for the message history
    socket.on("messageHistory", (data) => {
      // Set the message state to the input value
        // Loop over data.messages and decrypt each message, sender, and receiver
      setMessages(data.messages);
    });
  };

  return (
      <div className="flex h-[600px] w-full overflow-y-scroll">
        <div className="p-4 w-full">
          {messages.length > 0 ? (
        <ul>
          {messages.map((message, index) => (
            <li key={index} className="my-2">
              <div className={` ${message.from_user_id === sender ? 'text-right' : 'text-left'}`}>
                <div>From: {message.from_user_id}</div>
                <div>{message.message}</div>
              </div>
            </li>
          ))}
            {/* Typing Indicator */}
            {isTyping && (
                <li className={"my-2"}>
                    <p className={"text-right"}>{sender} is typing...</p>
                </li>
            )}
          {/* Reference for end of message list */}
          <div ref={messageEndRef} />
        </ul>
      ) : (
        <p className="font-bold text-center">Click on a chat to load messages</p>
      )}
    </div>
  </div>
);


}

export default MessageList;
