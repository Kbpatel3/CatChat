import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

function UserName() {
    const [userName, setUserName] = useState('');

    // Listen to the socket for a username
    useEffect(() => {
        socket.on('userName', (name) => {
            setUserName(name);
        });
    }, []);

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
