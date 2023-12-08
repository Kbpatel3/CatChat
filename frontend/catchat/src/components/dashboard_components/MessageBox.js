import { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { eventEmitter } from "../../events/EventEmitter";

const socket = io('http://localhost:5000');

function MessageBox({ sender }) {
  const [messageContent, setMessageContent] = useState('');


  const handleChange = (e) => {
    setMessageContent(e.target.value);
  }

  const handleEnterKeyPress = (e) => {
    if (e.key === 'Enter' && messageContent !== '') {
      // Set the message state to the input value
      eventEmitter.emit('messageSent', messageContent);
      setMessageContent('');  // Clears the text box after pressing enter
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
