class EventEmitter {
    constructor() {
        this.events = {};
    }

    on(eventName, listener) {
        if (!this.events[eventName]) {
            this.events[eventName] = [];
        }

        this.events[eventName].push(listener);
    }

    emit(event, data) {
        const listeners = this.events[event];

        if (listeners) {
            listeners.forEach(listener => {
                listener(data);
            });
        }
    }

    unsubscribe(eventName, listener) {
        if (!this.events[eventName]) {
            return;
        }

        const index = this.events[eventName].indexOf(listener);
        this.events[eventName].splice(index, 1);
    }
}

const eventEmitter = new EventEmitter();

export { eventEmitter }