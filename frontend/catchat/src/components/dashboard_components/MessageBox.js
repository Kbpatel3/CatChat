import { useState } from 'react';

function MessageBox() {
  const [message, setMessage] = useState('');

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      console.log('Message submitted:', message);

      // Send the message to the server via the socket connection // TODO
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