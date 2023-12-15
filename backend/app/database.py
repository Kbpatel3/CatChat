################################
# This file contains all the functions for interacting with the database.
# The database is used to store the users, chats, emails, passwords, connected clients,
# active rooms, and rooms and keys.
# The database is a SQLite database.
# @Author: Michael Imerman and Kaushal Patel
# @Version: 1.0
################################
import sqlite3


def connect_db():
    """
    This function connects to the database.
    :return: A connection to the database
    """
    return sqlite3.connect('catchat.db')


def create_tables():
    """
    This function creates the tables in the database.
    :return: None
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        email TEXT,
        password BLOB
    )''')

    # Chats Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chats (
        room_id TEXT,
        from_user_id BLOB,
        message BLOB
    )''')

    # Emails Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emails (
        email TEXT PRIMARY KEY
    )''')

    # Passwords Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        user_id TEXT PRIMARY KEY,
        password BLOB
    )''')

    # Connected Clients Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS connected_clients (
        user_id TEXT PRIMARY KEY
    )''')

    # Active Rooms Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS active_rooms (
        user_id TEXT,
        room_id TEXT
    )''')

    # Rooms and Keys Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms_and_keys (
        room_id TEXT PRIMARY KEY,
        key BLOB
    )''')

    conn.commit()
    conn.close()


def add_user(user_id, email, password):
    """
    This function adds a user to the database.
    :param user_id: The user id of the user
    :param email: The email of the user
    :param password: The password of the user
    :return: None
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users VALUES (?, ?, ?)', (user_id, email, password))
    conn.commit()
    conn.close()


# Additional functions for inserting and querying other data
def add_chat(room_id, from_user_id, message):
    """
    This function adds a chat to the database.
    :param room_id: The room id to which the chat belongs
    :param from_user_id: The id of the sender
    :param message: The message being sent
    :return: None
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO chats VALUES (?, ?, ?)', (room_id, from_user_id, message))
    conn.commit()
    conn.close()


def add_email(email):
    """
    This function adds an email to the database.
    :param email: The email to be added
    :return: None
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO emails VALUES (?)', (email,))
    conn.commit()
    conn.close()


def add_password(user_id, password):
    """
    This function adds a password to the database.
    :param user_id: The user id of the user whose password is being added
    :param password: THe password to be added
    :return: None
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passwords VALUES (?, ?)', (user_id, password))
    conn.commit()
    conn.close()


def add_connected_client(user_id):
    """
    This function adds a connected client to the database.
    :param user_id: The user id of the connected client
    :return: None
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO connected_clients VALUES (?)', (user_id,))
    conn.commit()
    conn.close()


def add_active_room(user_id, room_id):
    """
    This function adds an active room to the database.
    :param user_id: The user id of the user who is in the room
    :param room_id: The id of the room the user is in
    :return: None
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO active_rooms VALUES (?, ?)', (user_id, room_id))
    conn.commit()
    conn.close()


def add_room_and_key(room_id, key):
    """
    This function adds a room and its associated key to the database.
    :param room_id: The id of the room
    :param key: The key for the room
    :return: None
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rooms_and_keys VALUES (?, ?)', (room_id, key))
    conn.commit()
    conn.close()


def get_user(user_id):
    """
    This function gets a user from the database.
    :param user_id: The user id of the user to be retrieved
    :return: None
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_chat(room_id):
    """
    This function gets a chat from the database.
    :param room_id: The id of the room to which the chat belongs
    :return: None
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chats WHERE room_id = ?', (room_id,))
    chat = cursor.fetchall()
    conn.close()
    return chat


def get_active_rooms():
    """
    This function gets all the active rooms from the database.
    :return active_rooms: A list of all the active rooms
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM active_rooms')
    active_rooms = cursor.fetchall()
    conn.close()
    return active_rooms


def room_exists(room_id):
    """
    This function checks if a room exists in the database.
    :param room_id: The id of the room to be checked
    :return: count > 0 if the room exists, else count = 0
    """
    conn = connect_db()
    cursor = conn.cursor()
    # Use COUNT to check if the room exists and how many times
    cursor.execute('SELECT COUNT(*) FROM chats WHERE room_id = ?', (room_id,))
    # Fetch the count
    count = cursor.fetchone()[0]
    conn.close()
    # Return True if count is more than 0 (room exists), else False
    return count > 0


def is_room_active(room_id):
    """
    This function checks if a room is active in the database.
    :param room_id: The id of the room to be checked if it is active
    :return: count > 0 if the room is active, else count = 0
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM active_rooms WHERE room_id = ?', (room_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def email_exists(email):
    """
    This function checks if an email exists in the database.
    :param email: The email to be checked
    :return: count > 0 if the email exists, else count = 0
    """
    conn = connect_db()
    cursor = conn.cursor()
    # Use COUNT to check if the email exists and how many times
    cursor.execute('SELECT COUNT(*) FROM emails WHERE email = ?', (email,))
    # Fetch the count
    count = cursor.fetchone()[0]
    conn.close()
    # Return True if count is more than 0 (email exists), else False
    return count > 0


def get_emails():
    """
    This function gets all the emails from the database.
    :return emails: A list of all the emails
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM emails')
    emails = cursor.fetchall()
    # Extract the emails from the list of tuples
    emails = [email[0] for email in emails]
    conn.close()
    return emails


def get_password(user_id):
    """
    This function gets the password of a user from the database.
    :param user_id: The id of the user whose password is to be retrieved
    :return password: The password of the user
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM passwords WHERE user_id = ?', (user_id,))
    password = cursor.fetchone()
    conn.close()
    return password


def get_connected_client(user_id):
    """
    This function gets a connected client from the database.
    :param user_id: The id of the connected client to be retrieved
    :return connected_client: The connected client
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM connected_clients WHERE user_id = ?', (user_id,))
    connected_client = cursor.fetchone()
    conn.close()
    return connected_client


def get_connected_clients():
    """
    This function gets all the connected clients from the database.
    :return connected_clients: A list of all the connected clients
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM connected_clients')
    connected_clients = cursor.fetchall()
    # Extract the user_ids from the list of tuples
    connected_clients = [connected_client[0] for connected_client in connected_clients]
    conn.close()
    return connected_clients


def get_active_room(user_id):
    """
    This function gets the active room of a user from the database.
    :param user_id: The active room of the user to be retrieved
    :return: active_room: The active room of the user
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM active_rooms WHERE user_id = ?', (user_id,))
    active_room = cursor.fetchone()
    conn.close()
    return active_room


def get_room_and_key(room_id):
    """
    This function gets the key of a room from the database.
    :param room_id: The id of the room whose key is to be retrieved
    :return room_and_key: The room and the key of the room
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms_and_keys WHERE room_id = ?', (room_id,))
    room_and_key = cursor.fetchone()
    room_and_key = room_and_key[1]
    conn.close()
    return room_and_key


def drop_all_tables():
    """
    This function drops all the tables in the database.
    :return: None
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Drop all tables
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        print(f"Dropped table {table_name}")

    conn.commit()
    conn.close()


# Drop all tables and recreate them
drop_all_tables()
create_tables()
