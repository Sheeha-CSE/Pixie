import sqlite3
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

def get_db_connection():
    conn = sqlite3.connect(str(Config.DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table (Business Owners & Employees)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('owner', 'employee')),
        phone TEXT,
        interests TEXT DEFAULT '',
        avatar TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Business Profiles
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS business_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        business_name TEXT NOT NULL,
        industry TEXT NOT NULL,
        target_audience TEXT,
        location TEXT,
        budget REAL DEFAULT 0.0,
        products_services TEXT,
        contact_phone TEXT,
        contact_email TEXT,
        contact_whatsapp TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Marketing Campaigns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        channel TEXT NOT NULL,
        target_audience TEXT,
        budget REAL NOT NULL,
        spent REAL DEFAULT 0.0,
        duration_days INTEGER NOT NULL,
        status TEXT DEFAULT 'Active',
        reach INTEGER DEFAULT 0,
        clicks INTEGER DEFAULT 0,
        conversions INTEGER DEFAULT 0,
        assigned_employee_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (assigned_employee_id) REFERENCES users(id)
    )
    ''')

    # Employee Marketing Tasks / Jobs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER,
        assigned_employee_id INTEGER,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        channel TEXT NOT NULL,
        reward_inr REAL DEFAULT 500.0,
        tags TEXT DEFAULT '',
        status TEXT DEFAULT 'Available',
        proof_url TEXT,
        proof_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
        FOREIGN KEY (assigned_employee_id) REFERENCES users(id)
    )
    ''')

    # Customer Segments
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_segments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        segment_name TEXT NOT NULL,
        characteristics TEXT NOT NULL,
        customer_count INTEGER DEFAULT 0,
        avg_spend REAL DEFAULT 0.0,
        ai_strategy TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Competitor Analysis
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS competitor_analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        competitor_name TEXT NOT NULL,
        key_strengths TEXT NOT NULL,
        weaknesses TEXT,
        differentiation_strategy TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # AI Recommendation Engine items
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ai_recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        metric_issue TEXT NOT NULL,
        impact_text TEXT NOT NULL,
        ai_recommendation_text TEXT NOT NULL,
        action_category TEXT DEFAULT 'Strategy',
        is_dismissed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Pixie Chat Messages & History
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pixie_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        user_id INTEGER,
        sender TEXT NOT NULL,
        message TEXT NOT NULL,
        media_url TEXT,
        media_type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

# User Helpers
def create_user(name, email, password, role, phone="", interests=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role, phone, interests) VALUES (?, ?, ?, ?, ?, ?)",
            (name, email, password_hash, role, phone, interests)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user

def verify_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user['password_hash'], password):
        return user
    return None

def get_business_profile(user_id):
    conn = get_db_connection()
    profile = conn.execute("SELECT * FROM business_profiles WHERE user_id = ?", (user_id,)).fetchone()
    if not profile:
        # Check if there is any profile (for employee view, return the main business profile)
        profile = conn.execute("SELECT * FROM business_profiles ORDER BY id ASC LIMIT 1").fetchone()
    conn.close()
    return profile

def upsert_business_profile(user_id, business_name, industry, target_audience, location, budget, products_services, phone, email, whatsapp):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO business_profiles (user_id, business_name, industry, target_audience, location, budget, products_services, contact_phone, contact_email, contact_whatsapp, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(user_id) DO UPDATE SET
        business_name = excluded.business_name,
        industry = excluded.industry,
        target_audience = excluded.target_audience,
        location = excluded.location,
        budget = excluded.budget,
        products_services = excluded.products_services,
        contact_phone = excluded.contact_phone,
        contact_email = excluded.contact_email,
        contact_whatsapp = excluded.contact_whatsapp,
        updated_at = CURRENT_TIMESTAMP
    ''', (user_id, business_name, industry, target_audience, location, budget, products_services, phone, email, whatsapp))
    conn.commit()
    conn.close()

# Campaign Helpers
def get_campaigns(user_id=None):
    conn = get_db_connection()
    if user_id:
        campaigns = conn.execute("SELECT * FROM campaigns WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
    else:
        campaigns = conn.execute("SELECT * FROM campaigns ORDER BY created_at DESC").fetchall()
    conn.close()
    return campaigns

def create_campaign(user_id, title, channel, target_audience, budget, duration_days, assigned_employee_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO campaigns (user_id, title, channel, target_audience, budget, spent, duration_days, status, reach, clicks, conversions, assigned_employee_id)
    VALUES (?, ?, ?, ?, ?, 0.0, ?, 'Active', 0, 0, 0, ?)
    ''', (user_id, title, channel, target_audience, budget, duration_days, assigned_employee_id))
    campaign_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return campaign_id

# Employee Task Helpers
def get_employee_tasks(employee_id=None, status=None):
    conn = get_db_connection()
    query = """
    SELECT t.*, c.title as campaign_title, u.name as employee_name
    FROM employee_tasks t
    LEFT JOIN campaigns c ON t.campaign_id = c.id
    LEFT JOIN users u ON t.assigned_employee_id = u.id
    WHERE 1=1
    """
    params = []
    if employee_id:
        query += " AND (t.assigned_employee_id = ? OR t.assigned_employee_id IS NULL)"
        params.append(employee_id)
    if status:
        query += " AND t.status = ?"
        params.append(status)
    query += " ORDER BY t.created_at DESC"
    tasks = conn.execute(query, params).fetchall()
    conn.close()
    return tasks

def assign_task_to_employee(task_id, employee_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE employee_tasks SET assigned_employee_id = ?, status = 'In Progress' WHERE id = ?", (employee_id, task_id))
    conn.commit()
    conn.close()

def submit_task_proof(task_id, employee_id, proof_url, proof_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE employee_tasks SET proof_url = ?, proof_text = ?, status = 'Submitted' WHERE id = ? AND assigned_employee_id = ?",
                   (proof_url, proof_text, task_id, employee_id))
    conn.commit()
    conn.close()
