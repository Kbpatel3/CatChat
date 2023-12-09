/**
 * @class EventEmitter
 * @description A simple event emitter class (Observer pattern)
 * @constructor Creates a dictionary of events
 * @example This is how you can use it:
 * const eventEmitter = new EventEmitter();
 * eventEmitter.on('event', (data) => {
 *    console.log(data);
 * }
 * eventEmitter.emit('event', 'Hello world!');
 * // => 'Hello world!'
 */
class EventEmitter {
    /**
     * @constructor Creates a dictionary of events
     */
    constructor() {
        this.events = {};
    }

    /**
     * @method on Adds a listener to an event
     * @param eventName The name of the event
     * @param listener The listener function/callback
     */
    on(eventName, listener) {
        // If the event doesn't exist, create it
        if (!this.events[eventName]) {
            this.events[eventName] = [];
        }

        // Push the listener to the event
        this.events[eventName].push(listener);
    }

    /**
     * @method emit Emits an event
     * @param event The name of the event
     * @param data The data to pass to the listeners
     */
    emit(event, data) {
        // Get the listeners for the event
        const listeners = this.events[event];

        // If there are listeners, call them all
        if (listeners) {
            // For each listener, call it with the data
            listeners.forEach(listener => {
                listener(data);
            });
        }
    }

    /**
     * @method unsubscribe Removes a listener from an event
     * @param eventName The name of the event
     * @param listener The listener to remove
     */
    unsubscribe(eventName, listener) {
        // If the event doesn't exist, do nothing
        if (!this.events[eventName]) {
            return;
        }

        // Get the index of the listener
        const index = this.events[eventName].indexOf(listener);

        // If the listener exists, remove it
        this.events[eventName].splice(index, 1);
    }
}

// Create a single instance of the event emitter
const eventEmitter = new EventEmitter();

// Export the event emitter
export { eventEmitter }