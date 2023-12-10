// client/src/Dashboard.js
import React, { useState, useEffect } from 'react';
import { useLocation } from "react-router-dom";
import io from 'socket.io-client';
import MessageBox from "../dashboard_components/MessageBox.js";
import AppName from "../dashboard_components/AppName.js";
import SearchBar from "../dashboard_components/SearchBar.js";
import UserName from "../dashboard_components/UserName.js";
import ChatLists from "../dashboard_components/ChatLists.js";
import MessageList from "../dashboard_components/MessageList.js";

// Connect to the socket server
const socket = io('http://localhost:5000');

/**
 * Dashboard component
 * @returns {Element} Dashboard component
 */
function Dashboard() {
    // Use the location hook to get the user id
    const location = useLocation();

    // Get the user id from the location state
    const clientId = location.state.userId;

    // Set the client id
    const [client, setClient] = useState("");

    // Called on every render
    useEffect(() => {
        // Set the client id
        setClient(clientId);

        // Register user on the backend
        console.log("Connected");
        // Room name is the user id
        const roomName =  client;
        console.log("Room ID: " + roomName);

        // Join the room with the user id
        socket.emit('connection', roomName);
    });


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
            <div className={"row-span-5 col-start-1 row-start-3 flex-wrap justify-center h-full w-full bg-gray-200"}>
                <ChatLists client={client}></ChatLists>
            </div>
            <div className={"col-span-4 row-span-5 col-start-2 row-start-2 flex items-center justify-center h-full w-full bg-gray-200"}>
                <MessageList sender={client}></MessageList>
            </div>
            <div className={"col-span-4 col-start-2 row-start-7 flex items-center justify-center h-full w-full bg-gray-200"}>
                <MessageBox sender={client}></MessageBox>
            </div>
        </div>
    );
}

export default Dashboard;
