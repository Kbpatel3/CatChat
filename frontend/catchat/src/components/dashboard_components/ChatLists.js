import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import ChatRoomCard from './ChatRoomCard';

const socket = io('http://localhost:5000');

function ChatLists() {
    const [chatRooms, setChatRooms] = useState([]);

    useEffect(() => {
        // Listen to the socket for the list of chat rooms
        socket.on('chatRoomsList', (rooms) => {
            setChatRooms(rooms);
        });

        // Clean up the socket event listener on component unmount
        return () => {
            socket.off('chatRoomsList');
        };
    }, []);

    return (
        <div>
            {chatRooms.length === 0 ? (
                <div className="text-center text-gray-500">No Active Chats</div>
            ) : (
                <div>
                    {chatRooms.map((room) => (
                        <ChatRoomCard key={room.id} room={room} />
                    ))}
                </div>
            )}
        </div>
    );
}

export default ChatLists;
