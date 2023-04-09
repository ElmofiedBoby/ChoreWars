import uuid
from flask import Flask, jsonify, request
from dotenv import load_dotenv

import os
import psycopg2

load_dotenv()
app = Flask(__name__)
conn = psycopg2.connect(os.getenv('DB_URL'))

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
            user_score INTEGER,
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
            task_start DATE,
            task_complete BOOL,
            user_id INTEGER,
            room_code VARCHAR(6),
            FOREIGN KEY (user_id)
                REFERENCES Users (user_id),
            FOREIGN KEY (room_code)
                REFERENCES Rooms (room_code)
        );
    """)

    conn.commit()
    cur.close()

    return jsonify({
        'status': 'Database Initialized!'
    })

@app.route('/update/task', methods=['POST'])
def update_task():
    data = request.get_json()

    task_id = data['task_id']
    task_name = data['task_name']
    task_description = data['task_description']
    task_points = data['task_points']
    task_freq = data['task_freq']
    task_start = data['task_start']
    task_complete = data['task_complete']
    user_id = data['user_id']
    room_code = data['room_code']

    cur = conn.cursor()

    cur.execute("UPDATE Tasks SET task_name = %s WHERE task_id = %s", (task_name, task_id))
    cur.execute("UPDATE Tasks SET task_description = %s WHERE task_id = %s", (task_description, task_id))
    cur.execute("UPDATE Tasks SET task_points = %s WHERE task_id = %s", (task_points, task_id))
    cur.execute("UPDATE Tasks SET task_freq = %s WHERE task_id = %s", (task_freq, task_id))
    cur.execute("UPDATE Tasks SET task_start = %s WHERE task_id = %s", (task_start, task_id))
    cur.execute("UPDATE Tasks SET task_complete = %s WHERE task_id = %s", (task_complete, task_id))
    cur.execute("UPDATE Tasks SET user_id = %s WHERE task_id = %s", (user_id, task_id))
    cur.execute("UPDATE Tasks SET room_code = %s WHERE task_id = %s", (room_code, task_id))
    conn.commit()
    cur.close()

     # Return a success message
    return jsonify({'success': f'Task with ID {task_id} updated'}), 200


@app.route('/update/user', methods=['POST'])
def update_user():
    data = request.get_json()

    user_id = data['user_id']
    user_name = data['user_name']
    user_password = data['user_password']
    user_first = data['user_first']
    user_pfp = data['user_pfp']
    user_score = data['user_score']
    room_code = data['room_code']

    cur = conn.cursor()

    cur.execute("UPDATE Users SET user_name = %s WHERE user_id = %s", (user_name, user_id))
    cur.execute("UPDATE Users SET user_password = %s WHERE user_id = %s", (user_password, user_id))
    cur.execute("UPDATE Users SET user_password = %s WHERE user_id = %s", (user_first, user_id))
    cur.execute("UPDATE Users SET user_pfp = %s WHERE user_id = %s", (user_pfp, user_id))
    cur.execute("UPDATE Users SET user_score = %s WHERE user_id = %s", (user_score, user_id))
    cur.execute("UPDATE Users SET room_code = %s WHERE user_id = %s", (room_code, user_id))
    conn.commit()
    cur.close()

     # Return a success message
    return jsonify({'success': f'User with ID {user_id} updated'}), 200

@app.route('/update/room', methods=['POST'])
def update_room():
    data = request.get_json()

    room_code = data['room_code']
    room_name = data['room_name']
    room_limit = data['room_limit']

    cur = conn.cursor()

    cur.execute("UPDATE Rooms SET room_name = %s WHERE room_code = %s", (room_name, room_code))
    cur.execute("UPDATE Rooms SET room_limit = %s WHERE room_code = %s", (room_limit, room_code))
    conn.commit()
    cur.close()

     # Return a success message
    return jsonify({'success': f'Room with code {room_code} updated'}), 200

@app.route('/get/user/validate', methods=['POST'])
def validate_user():
    data = request.get_json()

    user_name = data['user_name']
    user_password = data['user_password']

    cur = conn.cursor()

    cur.execute("SELECT * FROM Users WHERE user_name = %s AND user_password = %s", (user_name, user_password,))
    result = cur.fetchone()

    if result:
        return jsonify({
            "success": True,
            "user_id": result[0]
        })
    else:
        return jsonify({
            "success": False,
            "user_id": None
        })

@app.route('/get/task', methods=[])
def get_task():
    task_id = request.args.get('task_id')

    cur = conn.cursor()

    # Query the Users table for the user with the specified user_id
    cur.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
    result = cur.fetchone()

    cur.close()

    # If a matching Task is found, return its data as a JSON response
    if result:
        task_data = {
            'task_id': result[0],
            'task_name': result[1],
            'task_description': result[2],
            'task_points': result[3],
            'task_freq': result[4],
            'task_start': result[5],
            'task_complete': result[6],
            'user_id': result[7],
            'room_code': result[8]
        }
        return jsonify(task_data)
    else:
        # If no matching User is found, return a 404 error
        return jsonify({'error': f'User with user_id {user_id} not found'}), 404

    

@app.route('/get/user', methods=['GET'])
def get_user():
    user_id = request.args.get('user_id')

    cur = conn.cursor()

    # Query the Users table for the user with the specified user_id
    cur.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
    result = cur.fetchone()

    cur.close()

    # If a matching User is found, return its data as a JSON response
    if result:
        user_data = {
            'user_id': result[0],
            'user_name': result[1],
            'user_password': result[2],
            'user_first': result[3],
            'user_pfp': result[4],
            'user_score': result[5],
            'room_code': result[6]
            
        }
        return jsonify(user_data)
    else:
        # If no matching User is found, return a 404 error
        return jsonify({'error': f'User with user_id {user_id} not found'}), 404
    

@app.route('/get/room/users', methods=['GET'])
def get_room_users():
    room_code = request.args.get('room_code')

    cur = conn.cursor()
    cur.execute('SELECT user_id FROM Users WHERE room_code = %s', (room_code,))
    result = cur.fetchall()
    cur.close()

    ids = []
    for row in result:
        ids.append(row[0])

    return jsonify(ids)

@app.route('/get/room/tasks', methods=['GET'])
def geT_room_tasks():
    room_code = request.args.get('room_code')

    cur = conn.cursor()
    cur.execute('SELECT task_id FROM Tasks WHERE room_code = %s', (room_code,))
    result = cur.fetchall()
    cur.close()

    ids = []
    for row in result:
        ids.append(row[0])

    return jsonify(ids)

@app.route('/get/room/all', methods=['GET'])
def get_all_rooms():
    cur = conn.cursor()

    cur.execute("SELECT * FROM Rooms")
    result = cur.fetchall()

    cur.close()

    rooms = []
    for row in result:
        room = {
            'room_code': row[0],
            'room_name': row[1],
            'room_limit': row[2]
        }
        rooms.append(room)
    return jsonify(rooms)

@app.route('/get/room', methods=['GET'])
def get_room():
    room_code = request.args.get('code')
    
    cur = conn.cursor()

    # Query the Rooms table for the room with the specified room_code
    cur.execute("SELECT * FROM Rooms WHERE room_code = %s", (room_code,))
    result = cur.fetchone()

    cur.close()

    # If a matching room is found, return its data as a JSON response
    if result:
        room_data = {
            'room_code': result[0],
            'room_name': result[1],
            'room_limit': result[2]
        }
        return jsonify(room_data)
    else:
        # If no matching room is found, return a 404 error
        return jsonify({'error': f'Room with room_code {room_code} not found'}), 404
    
@app.route('/get/leaderboard', methods=['GET'])
def get_leaderboard():
    room_code = request.args.get('room_code')

    return jsonify({
        "status": "endpoint incomplete :("
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
    user_name = data['user_name']
    user_password = data['user_password']
    user_first = data['user_first']
    user_pfp = data['user_pfp']
    user_score = 0

    cur = conn.cursor()

    # Insert the new user into the Users table
    cur.execute("""
        INSERT INTO Users (user_name, user_password, user_first, user_pfp, user_score)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING user_id;
    """, (user_name, user_password, user_first, user_pfp, user_score))

    user_id = cur.fetchone()[0]

    conn.commit()
    cur.close()

    return jsonify({
        "user_id": user_id,
        "username": user_name
    })

@app.route('/create/task', methods=['POST'])
def create_task():
    data = request.get_json()

    task_name = data['task_name']
    task_description = data['task_description']
    task_points = data['task_points']
    task_freq = data['task_freq']
    task_start = data['task_start']
    task_complete = data['task_complete']
    user_id = data['user_id']

    cur = conn.cursor()

    # Insert the new user into the Users table
    cur.execute("""
        INSERT INTO Tasks (task_name, task_description, task_points, task_freq, task_start, task_complete, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING task_id;
    """, (task_name, task_description, task_points, task_freq, task_start, task_complete, user_id))
    
    task_id = cur.fetchone()[0]

    conn.commit()
    cur.close()

    return jsonify({
        "task_id": task_id
    })


if __name__ == '__main__':
    app.run(debug=False, port=os.getenv('DB_PORT'))
