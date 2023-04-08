import uuid
from flask import Flask, jsonify, request
from dotenv import load_dotenv

import os
import psycopg2

load_dotenv()
app = Flask(__name__)
conn = psycopg2.connect(os.getenv('DATABASE_URL'))

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/initialize')
def init():

    cur = conn.cursor()

    # Drop the existing tables, if they exist
    cur.execute("""
        DROP TABLE IF EXISTS Users CASCADE;
        DROP TABLE IF EXISTS Tasks CASCADE;
        DROP TABLE IF EXISTS Rooms CASCADE;
    """)

    # Create the Rooms table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Rooms (
            room_code VARCHAR(6) PRIMARY KEY,
            room_name VARCHAR(255),
            room_limit INTEGER
        );
    """)

    # Create the Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255),
            user_password VARCHAR(255),
            user_first BOOL,
            user_pfp VARCHAR(255),
            room_code VARCHAR(6),
            FOREIGN KEY (room_code)
                REFERENCES Rooms (room_code)
        );
    """)

    # Create the Tasks table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
            task_id SERIAL PRIMARY KEY,
            task_name VARCHAR(255),
            task_description VARCHAR(255),
            task_points INTEGER,
            task_freq INTEGER,
            user_id INTEGER,
            FOREIGN KEY (user_id)
                REFERENCES Users (user_id)
        );
    """)

    conn.commit()
    cur.close()

    return jsonify({
        'status': 'Database Initialized!'
    })

@app.route('/create/task', methods=['POST'])
def create_task():
    data = request.get_json()

    task_name = data['task_name']
    task_description = data['task_description']
    task_points = data['task_points']
    task_freq = data['task_freq']
    user_id = data['user_id']

    cur = conn.cursor()

    # Insert the new user into the Users table
    cur.execute("""
        INSERT INTO Tasks (task_name, task_description, task_points, task_freq, user_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING task_id;
    """, (task_name, task_description, task_points, task_freq, user_id))
    
    task_id = cur.fetchone()[0]

    conn.commit()
    cur.close()

    return jsonify({
        "task_id": task_id
    })


@app.route('/create/room', methods=['POST'])
def create_room():
    data = request.get_json()

    room_code = str(uuid.uuid4().hex)[:6]
    room_name = data['room_name']
    room_limit = data['room_limit']

    cur = conn.cursor()

    # Insert the new user into the Users table
    cur.execute("""
        INSERT INTO Rooms (room_code, room_name, room_limit)
        VALUES (%s, %s, %s)
        RETURNING room_code;
    """, (room_code, room_name, room_limit))
    
    room_code = cur.fetchone()[0]

    conn.commit()
    cur.close()

    return jsonify({
        "room_code": room_code
    })

@app.route('/create/user', methods=['POST'])
def create_user():
    data = request.get_json()

    # Get the user data from the request
    username = data['username']
    password = data['password']
    isFirst = data['isFirst']
    pfp_path = data['pfp_path']

    cur = conn.cursor()

    # Insert the new user into the Users table
    cur.execute("""
        INSERT INTO Users (user_name, user_password, user_first, user_pfp)
        VALUES (%s, %s, %s, %s)
        RETURNING user_id;
    """, (username, password, isFirst, pfp_path))

    user_id = cur.fetchone()[0]

    conn.commit()
    cur.close()

    return jsonify({
        "user_id": user_id,
        "username": username
    })


if __name__ == '__main__':
    app.run(debug=True, )
