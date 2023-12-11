import React from 'react';
import io from "socket.io-client";
import { eventEmitter } from '../../events/EventEmitter'

// Create a socket connection to the server
const socket = io('http://localhost:5000');

/**
 * This component represents a single chat room card
 * @param userId The user id that corresponds to who the card is for
 * @param client The user id of the client that can click on the card
 * @returns {Element} The chat room card
 */
const ChatRoomCard = ({ userId, client }) => {

    /**
     * This function handles when a card is clicked on.
     * @param userId The user id that corresponds to the card that was clicked on
     */
    const handleCardClick = (userId) => {
        // console.log("Clicked on " + userId);
        // console.log("From " + client);

        // Create a room name by concatenating the client and user id
        const roomName = client + "." + userId;

        // Call the createRoom event on the server passing in the client, room name, and user id
        socket.emit('createRoom', {client, roomName, userId});
        // console.log("Created room " + roomName)

        // Notify subscribers that a card has been clicked
        // console.log("Emitting cardClicked event")
        eventEmitter.emit('cardClicked', userId);
        // console.log("Emitted cardClicked event")
    };

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
