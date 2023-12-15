import sqlite3


def connect_db():
    return sqlite3.connect('catchat.db')


def create_tables():
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
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users VALUES (?, ?, ?)', (user_id, email, password))
    conn.commit()
    conn.close()


# Additional functions for inserting and querying other data
def add_chat(room_id, from_user_id, message):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO chats VALUES (?, ?, ?)', (room_id, from_user_id, message))
    conn.commit()
    conn.close()


def add_email(email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO emails VALUES (?)', (email,))
    conn.commit()
    conn.close()


def add_password(user_id, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passwords VALUES (?, ?)', (user_id, password))
    conn.commit()
    conn.close()


def add_connected_client(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO connected_clients VALUES (?)', (user_id,))
    conn.commit()
    conn.close()


def add_active_room(user_id, room_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO active_rooms VALUES (?, ?)', (user_id, room_id))
    conn.commit()
    conn.close()


def add_room_and_key(room_id, key):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rooms_and_keys VALUES (?, ?)', (room_id, key))
    conn.commit()
    conn.close()


def get_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_chat(room_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chats WHERE room_id = ?', (room_id,))
    chat = cursor.fetchall()
    conn.close()
    return chat

def get_active_rooms():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM active_rooms')
    active_rooms = cursor.fetchall()
    conn.close()
    return active_rooms

def room_exists(room_id):
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
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM active_rooms WHERE room_id = ?', (room_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0



def email_exists(email):
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
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM emails')
    emails = cursor.fetchall()
    # Extract the emails from the list of tuples
    emails = [email[0] for email in emails]
    conn.close()
    return emails


def get_password(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM passwords WHERE user_id = ?', (user_id,))
    password = cursor.fetchone()
    conn.close()
    return password


def get_connected_client(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM connected_clients WHERE user_id = ?', (user_id,))
    connected_client = cursor.fetchone()
    conn.close()
    return connected_client


def get_connected_clients():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM connected_clients')
    connected_clients = cursor.fetchall()
    # Extract the user_ids from the list of tuples
    connected_clients = [connected_client[0] for connected_client in connected_clients]
    conn.close()
    return connected_clients


def get_active_room(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM active_rooms WHERE user_id = ?', (user_id,))
    active_room = cursor.fetchone()
    conn.close()
    return active_room


def get_room_and_key(room_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms_and_keys WHERE room_id = ?', (room_id,))
    room_and_key = cursor.fetchone()
    room_and_key = room_and_key[1]
    conn.close()
    return room_and_key


def drop_all_tables():
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
