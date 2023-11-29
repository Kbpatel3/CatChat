// client/src/Dashboard.js
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import MessageBox from "../dashboard_components/MessageBox.js";
import AppName from "../dashboard_components/AppName.js";
import SearchBar from "../dashboard_components/SearchBar.js";
import UserName from "../dashboard_components/UserName.js";
import ChatLists from "../dashboard_components/ChatLists.js";

const socket = io('http://localhost:5000');

function Dashboard(UserId) {
    socket.on('connect', () => {
        console.log("Connected");

        // Join the room with the user id
        socket.emit('join', UserId);
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
