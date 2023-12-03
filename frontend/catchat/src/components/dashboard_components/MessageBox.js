import { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { eventEmitter } from "../../events/EventEmitter";

const socket = io('http://localhost:5000');

function MessageBox({ sender }) {
  const [message, setMessage] = useState('');



  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      // Set the message state to the input value
      setMessage(sender + ": " + message);

      // // Add to the messages array
      // setMessages([...messages, message]);
      //
      // // Emit the message to the server
      // socket.emit('message', message);


    }
  };

  return (
    <div className="p-4 w-full h-full">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your message and press Enter"
        className="border border-gray-400 p-2 w-full"
      />
    </div>
  );
}

export default MessageBox;
