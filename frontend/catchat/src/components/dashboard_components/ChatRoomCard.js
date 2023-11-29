import React from 'react';

const ChatRoomCard = ({ room }) => {
    return (
        <div className="bg-purple-500 p-4 m-2 rounded-md">
            <p className="text-white">{room.name}</p>
        </div>
    );
};

export default ChatRoomCard;
