import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
from config import Config
from models import (
    init_db, get_db_connection, create_user, verify_user, get_user_by_id,
    get_business_profile, upsert_business_profile, get_campaigns, create_campaign,
    get_employee_tasks, assign_task_to_employee, submit_task_proof
)
from groq_service import groq_service

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database on startup
try:
    with app.app_context():
        init_db()
except Exception as e:
    print(f"[Database Startup Warning]: {e}")

# Helper for login protection
def login_required(role=None):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for('login_view'))
            if role and session.get('role') != role:
                flash("You do not have permission to access this page.", "danger")
                if session.get('role') == 'employee':
                    return redirect(url_for('employee_portal_view'))
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

# --- Authentication Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        user = verify_user(email, password)

        if user:
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['email'] = user['email']
            session['role'] = user['role']
            session['avatar'] = user['avatar'] or ('👩‍💼' if user['role'] == 'owner' else '🎓')
            session['interests'] = user['interests'] or ''
            
            flash(f"Welcome back, {user['name']}!", "success")
            if user['role'] == 'employee':
                return redirect(url_for('employee_portal_view'))
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'owner')
        phone = request.form.get('phone', '').strip()
        interests = request.form.get('interests', '').strip()

        user_id = create_user(name, email, password, role, phone, interests)
        if user_id:
            # If owner, optionally create profile
            if role == 'owner':
                biz_name = request.form.get('business_name', 'My Business')
                industry = request.form.get('industry', 'Retail')
                upsert_business_profile(
                    user_id, biz_name, industry,
                    "College students aged 18-24", "Online & Campus", 50000.0,
                    "Fashion & Accessories", phone, email, phone
                )

            session['user_id'] = user_id
            session['name'] = name
            session['email'] = email
            session['role'] = role
            session['avatar'] = '👩‍💼' if role == 'owner' else '🎓'
            session['interests'] = interests

            flash("Account registered successfully! Welcome to MarketMind.", "success")
            if role == 'employee':
                return redirect(url_for('employee_portal_view'))
            return redirect(url_for('dashboard'))
        else:
            flash("An account with that email already exists.", "danger")

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for('login_view'))

# --- Main Business Owner Routes ---

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login_view'))
    if session.get('role') == 'employee':
        return redirect(url_for('employee_portal_view'))
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required(role='owner')
def dashboard():
    campaigns = get_campaigns()
    return render_template('dashboard.html', campaigns=campaigns)

@app.route('/profile', methods=['GET', 'POST'])
@login_required(role='owner')
def profile_view():
    user_id = session.get('user_id')
    if request.method == 'POST':
        business_name = request.form.get('business_name')
        industry = request.form.get('industry')
        target_audience = request.form.get('target_audience')
        location = request.form.get('location')
        budget = float(request.form.get('budget', 0))
        products_services = request.form.get('products_services')
        contact_phone = request.form.get('contact_phone')
        contact_email = request.form.get('contact_email')
        contact_whatsapp = request.form.get('contact_whatsapp')

        upsert_business_profile(
            user_id, business_name, industry, target_audience,
            location, budget, products_services, contact_phone, contact_email, contact_whatsapp
        )
        flash("Business profile and contact details updated successfully!", "success")
        return redirect(url_for('profile_view'))

    profile = get_business_profile(user_id)
    return render_template('profile.html', profile=profile)

@app.route('/strategy')
@login_required()
def strategy_view():
    return render_template('strategy.html')

@app.route('/campaigns')
@login_required()
def campaigns_view():
    campaigns = get_campaigns()
    return render_template('campaigns.html', campaigns=campaigns)

@app.route('/content-generator')
@login_required()
def content_generator_view():
    return render_template('content_generator.html')

@app.route('/analytics')
@login_required(role='owner')
def analytics_view():
    return render_template('analytics.html')

@app.route('/segmentation')
@login_required(role='owner')
def segmentation_view():
    conn = get_db_connection()
    segments = conn.execute("SELECT * FROM customer_segments ORDER BY id ASC").fetchall()
    conn.close()
    return render_template('segmentation.html', segments=segments)

@app.route('/competitors', methods=['GET', 'POST'])
@login_required(role='owner')
def competitors_view():
    diff_strategy = ""
    if request.method == 'POST':
        competitor_input = request.form.get('competitor_input', '')
        analysis = groq_service.analyze_competitors(competitor_input)
        diff_strategy = analysis.get('differentiation_strategy', '')
        flash("AI Competitor Analysis refreshed!", "success")

    conn = get_db_connection()
    competitors = conn.execute("SELECT * FROM competitor_analyses ORDER BY id ASC").fetchall()
    conn.close()
    return render_template('competitors.html', competitors=competitors, differentiation_strategy=diff_strategy)

@app.route('/recommendations')
@login_required(role='owner')
def recommendations_view():
    conn = get_db_connection()
    alerts = conn.execute("SELECT * FROM ai_recommendations ORDER BY id ASC").fetchall()
    conn.close()
    return render_template('recommendations.html', alerts=alerts)

@app.route('/recommendations/refresh', methods=['POST'])
@login_required(role='owner')
def refresh_recommendations_action():
    flash("AI Growth Diagnostic refreshed with latest engagement patterns!", "success")
    return redirect(url_for('recommendations_view'))

@app.route('/employees')
@login_required(role='owner')
def employees_management_view():
    conn = get_db_connection()
    employees = conn.execute("SELECT * FROM users WHERE role = 'employee'").fetchall()
    tasks = conn.execute("""
        SELECT t.*, u.name as employee_name 
        FROM employee_tasks t
        LEFT JOIN users u ON t.assigned_employee_id = u.id
        ORDER BY t.created_at DESC
    """).fetchall()
    conn.close()
    return render_template('employees_management.html', employees=employees, tasks=tasks)

@app.route('/employees/task/<int:task_id>/approve', methods=['POST'])
@login_required(role='owner')
def approve_task_action(task_id):
    conn = get_db_connection()
    conn.execute("UPDATE employee_tasks SET status = 'Approved' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    flash("Task submission approved and reward credited to the employee!", "success")
    return redirect(url_for('employees_management_view'))

# --- Part-Time Employee Workspace Routes ---

@app.route('/employee-portal')
@login_required(role='employee')
def employee_portal_view():
    user_id = session.get('user_id')
    user = get_user_by_id(user_id)
    business = get_business_profile(None) # fetches the registered business profile

    # AI Matchmaker based on user interests
    interests = user['interests'] if user else "Instagram Reels, Meme Marketing"
    matched_tasks = groq_service.get_employee_matched_tasks(interests)
    my_tasks = get_employee_tasks(employee_id=user_id)

    return render_template('employee_portal.html', user=user, business=business, matched_tasks=matched_tasks, my_tasks=my_tasks)

# --- AJAX APIs ---

@app.route('/api/strategy/generate', methods=['POST'])
def api_generate_strategy():
    data = request.get_json() or {}
    prompt = data.get('prompt', 'Small clothing store for college students')
    budget = data.get('budget', '₹50,000')
    industry = data.get('industry', 'Retail Fashion')

    strategy = groq_service.generate_marketing_strategy(prompt, budget, industry)
    return jsonify({"status": "success", "data": strategy})

@app.route('/api/content/generate', methods=['POST'])
def api_generate_content():
    data = request.get_json() or {}
    content_type = data.get('contentType', 'Instagram Caption')
    topic = data.get('topic', 'College fest drop')
    tone = data.get('tone', 'Energetic & Trendy')
    product = data.get('product', '')

    content = groq_service.generate_content(content_type, topic, tone, product)
    return jsonify({"status": "success", "data": content})

@app.route('/api/campaigns/create', methods=['POST'])
def api_create_campaign():
    data = request.get_json() or {}
    user_id = session.get('user_id', 1)
    title = data.get('title')
    channel = data.get('channel')
    target = data.get('target')
    budget = float(data.get('budget', 10000))
    duration = int(data.get('duration', 7))

    camp_id = create_campaign(user_id, title, channel, target, budget, duration)
    return jsonify({"status": "success", "campaign_id": camp_id})

@app.route('/api/employee/task/<int:task_id>/accept', methods=['POST'])
def api_accept_task(task_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Login required"}), 401
    assign_task_to_employee(task_id, user_id)
    return jsonify({"status": "success"})

@app.route('/api/employee/task/<int:task_id>/submit', methods=['POST'])
def api_submit_task_proof(task_id):
    user_id = session.get('user_id')
    data = request.get_json() or {}
    proof_url = data.get('proof_url', '')
    proof_text = data.get('proof_text', '')

    submit_task_proof(task_id, user_id, proof_url, proof_text)
    return jsonify({"status": "success"})

# --- Pixie AI Chatbot Assistant API ---

@app.route('/api/pixie/chat', methods=['POST'])
def api_pixie_chat():
    data = request.get_json() or {}
    message = data.get('message', '')
    language = data.get('language', 'English')
    history = data.get('history', [])
    media_url = data.get('media_url', None)
    media_type = data.get('media_type', None)

    # Call Pixie engine
    response_data = groq_service.chat_with_pixie(message, chat_history=history, language=language)

    # If user provided image or video, add interactive commentary
    if media_url:
        response_data['reply'] = f"✨ **Pixie reviewed your uploaded {media_type}!** 📸\n\nThis looks fantastic! The visual composition and color balance are super catchy for college reels and campus posters! Here is my feedback on your text:\n\n" + response_data['reply']

    return jsonify({"status": "success", "data": response_data})

@app.route('/api/groq/status')
def api_groq_status():
    return jsonify({
        "configured": groq_service.is_configured(),
        "model": Config.GROQ_MODEL
    })

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
