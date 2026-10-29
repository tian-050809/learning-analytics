import sqlite3
import hashlib

DB = "project2.db"

def get_conn():
    conn = sqlite3.connect(DB, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password_hash TEXT, role TEXT, student_id TEXT
    );
    CREATE TABLE IF NOT EXISTS suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT, rule_id TEXT, 
        original_text TEXT, modified_text TEXT, teacher_name TEXT, created_at TEXT
    );
    """)
    conn.commit()
    conn.close()

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username, password, role, student_id=None):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO users(username,password_hash,role,student_id) VALUES(?,?,?,?)",
                     (username, hash_pw(password), role, student_id))
        conn.commit()
        return True, "注册成功"
    except sqlite3.IntegrityError:
        return False, "用户名已存在"
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, hash_pw(password))).fetchone()
    conn.close()
    return dict(row) if row else None

def save_suggestion(student_id, rule_id, orig, mod, teacher, time):
    conn = get_conn()
    conn.execute("INSERT INTO suggestions(student_id,rule_id,original_text,modified_text,teacher_name,created_at) VALUES(?,?,?,?,?,?)",
                 (student_id, rule_id, orig, mod, teacher, time))
    conn.commit()
    conn.close()

def get_suggestions(student_id=None):
    conn = get_conn()
    if student_id:
        rows = conn.execute("SELECT * FROM suggestions WHERE student_id=? ORDER BY id DESC", (student_id,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM suggestions ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
