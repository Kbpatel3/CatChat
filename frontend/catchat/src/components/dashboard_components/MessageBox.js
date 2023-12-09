import { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { eventEmitter } from "../../events/EventEmitter";

// Create a socket connection to the server
const socket = io('http://localhost:5000');

/**
 * This component renders the message box at the bottom of the dashboard. The one that you type in.
 * @param sender The user ID of the user that is sending the message
 * @returns {JSX.Element} The message box component
 */
function MessageBox({ sender }) {
  // The message state is the message that the user is typing
  const [messageContent, setMessageContent] = useState('');


  /**
   * This function is called when the content of the message box changes.
   * @param e The event object which contains the new value of the message box
   */
  const handleChange = (e) => {
    // Set the message state to the input value
    setMessageContent(e.target.value);
  }

  /**
   * This function is called when the user presses a key while the message box is in focus. We only care about the enter key.
   * @param e The event object which contains the key that was pressed
   */
  const handleEnterKeyPress = (e) => {
    // If the enter key was pressed and the message box is not empty
    if (e.key === 'Enter' && messageContent !== '') {
      // Create an event called 'messageSent' and pass the message content as the payload
      eventEmitter.emit('messageSent', messageContent);

      // Clear the message box by setting the message state to an empty string
      setMessageContent('');
    }
  }

  return (
    <div className="p-4 w-full h-full">
      <input
        type="text"
        value={messageContent}
        onChange={handleChange}
        onKeyDown={handleEnterKeyPress}
        placeholder="Type your message and press Enter"
        className="border border-gray-400 p-2 w-full"
      />
    </div>
  );
}

export default MessageBox;
