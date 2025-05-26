from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Initialisation simple de la base SQLite (en mémoire pour l'exemple)
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/message', methods=['GET'])
def get_message():
    conn = get_db_connection()
    message = conn.execute('SELECT content FROM messages WHERE id = 1').fetchone()
    conn.close()
    if message:
        return jsonify({'message': message['content']})
    else:
        return jsonify({'message': 'Aucun message trouvé'}), 404

@app.route('/api/message', methods=['POST'])
def update_message():
    new_message = request.json.get('message')
    conn = get_db_connection()
    conn.execute('UPDATE messages SET content = ? WHERE id = 1', (new_message,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Message mis à jour'})

if __name__ == '__main__':
    # Création de la table et insertion d'un message initial (à lancer une fois)
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, content TEXT)')
    # Insert initial message if not exists
    cur = conn.execute('SELECT * FROM messages WHERE id = 1')
    if not cur.fetchone():
        conn.execute('INSERT INTO messages (id, content) VALUES (1, "Message initial depuis la base SQLite")')
    conn.commit()
    conn.close()

    app.run(debug=True)
