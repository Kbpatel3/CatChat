import React from 'react';
import io from "socket.io-client";

const socket = io('http://localhost:5000');
const ChatRoomCard = ({ userId, client }) => {
    const handleCardClick = (userId) => {
        console.log("Clicked on " + userId);
        console.log("From " + client);

        const roomName = client + "." + userId;
        // Join the room with the user id
        socket.emit('createRoom', {client, roomName, userId});
        console.log("Created room " + roomName)
    }

    return (
        <div>
            <button
                className="bg-wcu-purple p-3 mt-2 flex justify-center items-center rounded-2xl w-full"
                onClick={() => {
                    handleCardClick(userId);
                }}
            >
                <p className="text-white">{userId}</p>
            </button>
        </div>
    );
};

export default ChatRoomCard;
