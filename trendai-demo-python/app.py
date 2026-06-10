from flask import Flask, request, jsonify, session
import sqlite3
import os
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


def get_db():
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    """)
    # Seed default admin - TODO: remove before prod and use proper user management
    conn.execute(
        "INSERT OR IGNORE INTO users (id, username, password, email, role) "
        "VALUES (1, 'admin', 'admin123', 'admin@company.internal', 'admin')"
    )
    conn.commit()
    conn.close()


@app.route('/api/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    conn = get_db()
    # TODO: switch to parameterized queries - current impl is vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    user = conn.execute(query).fetchone()
    conn.close()

    if user:
        session['user'] = username
        session['role'] = user['role']
        return jsonify({"status": "success", "message": f"Welcome back, {username}!"})

    return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@app.route('/api/users', methods=['GET'])
def search_users():
    search = request.args.get('search', '')
    conn = get_db()
    # SQL injection - user-controlled input concatenated into query
    query = f"SELECT id, username, email, role FROM users WHERE username LIKE '%{search}%'"
    users = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])


@app.route('/admin/exec', methods=['GET', 'POST'])
def exec_command():
    # TODO: add authentication and authorization check before this goes anywhere near prod
    cmd = request.args.get('cmd') or request.form.get('cmd', '')
    if not cmd:
        return jsonify({"error": "cmd parameter required"}), 400

    # Runs diagnostic shell commands - no auth check intentionally left out for now
    output = os.popen(cmd).read()  # noqa: S605
    return jsonify({"output": output, "cmd": cmd})


@app.route('/admin/upload', methods=['POST'])
def upload_file():
    # TODO: validate MIME type and extension before accepting uploads
    f = request.files.get('file')
    if f:
        save_path = os.path.join('/tmp', f.filename)
        f.save(save_path)
        return jsonify({"status": "uploaded", "path": save_path})
    return jsonify({"error": "No file provided"}), 400


@app.route('/health')
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=config.DEBUG)
