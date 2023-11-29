// client/src/Dashboard.js
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import MessageBox from "../dashboard_components/MessageBox.js";
import AppName from "../dashboard_components/AppName.js";
import SearchBar from "../dashboard_components/SearchBar.js";
import UserName from "../dashboard_components/UserName.js";
import ChatLists from "../dashboard_components/ChatLists.js";

const socket = io('http://localhost:5000');

function Dashboard() {
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState('');
    const [user, setUser] = useState('');
    const [room, setRoom] = useState('');
    const [activeChats, setActiveChats] = useState([]);

    function confirmPrivateChatRequest(sender) {
        const confirm = window.confirm; // Explicitly define confirm function
        const message = `${sender} wants to start a private chat with you. Do you accept?`;

        if (confirm(message)) {
            socket.emit('privateChatAccept', { sender });
        } else {
            socket.emit('privateChatDecline', { sender });
        }
    }



    useEffect(() => {
        // Listen for incoming messages
        socket.on('message', (data) => {
            setMessages((prevMessages) => [...prevMessages, data]);
        });

        // Listen for updates to the list of active chats
        socket.on('updateActiveChats', (chats) => {
            console.log('Received updated active chats:', chats);
            setActiveChats(chats);
        });

        // Listen for private chat requests
        socket.on('privateChatRequestReceived', (data) => {
            const sender = data.sender;
            confirmPrivateChatRequest(sender)
        });


        // Listen for private chat acceptances
        socket.on('privateChatEstablished', (data) => {
            const chatRoom = data.sender;
            setRoom(chatRoom);
            // Display the private chat interface
        });

        // Clean up the socket connection when the component unmounts
        return () => {
            socket.disconnect();
        };
    }, []);


    const sendMessage = () => {
        if (message.trim() !== '') {
            socket.emit('message', { user, message, room });
            setMessage('');
        }
    };

    const joinRoom = (chatRoom) => {
        // Emit a 'join' event to the server when joining a room
        socket.emit('join', { user, room: chatRoom });
        setRoom(chatRoom);
    };

    const startPrivateChat = (chatRoom) => {
        // Emit a 'startPrivateChat' event to the server when starting a private chat
        socket.emit('startPrivateChat', { user, chatRoom });
        setRoom(chatRoom);
    };

    const handleUserClick = (chatRoom) => {
    if (chatRoom !== room) {
        // Check if the selected user is online
        if (activeChats.includes(chatRoom)) {
            // Start a private chat with the selected user
            socket.emit('privateChatRequest', { receiver: chatRoom });
        } else {
            alert('Selected user is not online');
        }
    }
};


    return (
        <div className={"grid grid-cols-5 grid-rows-7 gap-2 h-screen w-screen"}>
            <div className={"flex items-center justify-center h-full w-full bg-gray-200"}>
                <AppName></AppName>
            </div>
            <div className={"col-span-4 flex items-center justify-center h-full w-full bg-gray-200"}>
                <UserName></UserName>
            </div>
            <div className={"row-start-2 flex items-center justify-center h-full w-full bg-gray-200"}>
                <SearchBar></SearchBar>
            </div>
            <div className={"row-span-5 col-start-1 row-start-3 flex items-center justify-center h-full w-full bg-gray-200"}>
                <ChatLists></ChatLists>
            </div>
            <div className={"col-span-4 row-span-5 col-start-2 row-start-2 flex items-center justify-center h-full w-full bg-gray-200"}>5</div>
            <div className={"col-span-4 col-start-2 row-start-7 flex items-center justify-center h-full w-full bg-gray-200"}>
                <MessageBox></MessageBox>
            </div>
        </div>
    );
}

export default Dashboard;
