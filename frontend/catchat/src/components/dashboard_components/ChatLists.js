import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import ChatRoomCard from './ChatRoomCard';

// Create a socket connection to the server
const socket = io('http://localhost:5000');

/**
 * ChatLists component. This component renders a list of chat rooms on the left side of the dashboard.
 * @param client - The client's username that is the owner of the dashboard
 * @returns {Element} - Returns the JSX element that renders the chat rooms
 */
function ChatLists({client}) {
    // State variable to store the chat rooms list from the server
    const [chatRooms, setChatRooms] = useState([]);

    // On component mount, get the chat rooms from the server by calling the getConnectedClients event
    // Dependent on the chatRooms state variable
    useEffect(() => {
        // Call server's getConnectedClients event
        socket.emit('getConnectedClients');

        // When the server responds with the list of chat rooms, set the chatRooms state variable
        socket.on('ConnectedClients', (data) => {
            setChatRooms(data.clients);
        });
    });

    return (
        <div>
            {chatRooms.length === 0 ? (
                <div className="text-center text-gray-500">No Active Clients</div>
            ) : (
                <div className={"max-h-[43rem] overflow-y-auto"}>
                    {chatRooms.map((room) => (
                        <ChatRoomCard userId={room} client={client}/>
                    ))}
                </div>
            )}
        </div>
    );
}

export default ChatLists;
