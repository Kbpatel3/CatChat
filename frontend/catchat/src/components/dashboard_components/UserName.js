import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import {eventEmitter} from "../../events/EventEmitter";

// Connect to the socket
const socket = io('http://localhost:5000');

/**
 * This component renders the user's username.
 * @returns {Element} The user's username.
 */
function UserName() {
    // State for the username
    const [userName, setUserName] = useState('');

    // Listen to the socket for a username
    useEffect(() => {
        // Listen for card click event to correctly display the username of the person that the user is chatting with

        eventEmitter.on('cardClicked', (userId) => {
            // Set the username state to the user id of the person that the user is chatting with
            setUserName(userId);
        });
    });

    return (
        <div className="w-full h-full flex items-center justify-center">
            <div className="text-center text-wcu-gold text-4xl">
                {userName !== '' ? (
                    // If userName is not empty, render the actual userName
                    userName
                ) : (
                    // If userName is empty, render a placeholder text
                    <span className="text-wcu-gold">Username</span>
                )}
            </div>
        </div>
    );
}

export default UserName;
