import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import ChatRoomCard from './ChatRoomCard';

const socket = io('http://localhost:5000');

function ChatLists({client}) {
    const [chatRooms, setChatRooms] = useState([]);
    useEffect(() => {
        //console.log("Getting chat rooms from server")
        socket.emit('getConnectedClients');

        // Call server's getChatRooms event
        socket.once('ConnectedClients', (data) => {
            setChatRooms(data.clients);
        });
    }, [chatRooms]);

    return (
        <div>
            {chatRooms.length === 0 ? (
                <div className="text-center text-gray-500">No Active Clients</div>
            ) : (
                <div>
                    {chatRooms.map((room) => (
                        <ChatRoomCard userId={room} client={client}/>
                    ))}
                </div>
            )}
        </div>
    );
}

export default ChatLists;
