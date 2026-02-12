import sqlite3

DB_NAME = "intranet.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, salary INTEGER)")
    # Admin / admin123
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin', 50000)")
    # Guest / guest
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'guest', 'guest', 'user', 20000)")
    conn.commit()
    conn.close()

def check_login(user, password):
    # VULN: SQL Injection Clásica
    conn = sqlite3.connect(DB_NAME)
    # Fíjate que devolvemos un objeto Row para acceder por nombre
    conn.row_factory = sqlite3.Row 
    
    # El becario usó f-strings... mal asunto.
    query = f"SELECT * FROM users WHERE username = '{user}' AND password = '{password}'"
    print(f"[DEBUG] Executing: {query}") 
    
    return conn.execute(query).fetchone()

def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    # VULN: IDOR (No verifica quién pide el dato) + SQLi potencial
    return conn.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()
