import sqlite3
from werkzeug.security import generate_password_hash
from models import init_db, get_db_connection
from config import Config

def seed_database(skip_init=False):
    if not skip_init:
        init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing to ensure fresh seed
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM business_profiles")
    cursor.execute("DELETE FROM campaigns")
    cursor.execute("DELETE FROM employee_tasks")
    cursor.execute("DELETE FROM customer_segments")
    cursor.execute("DELETE FROM competitor_analyses")
    cursor.execute("DELETE FROM ai_recommendations")
    cursor.execute("DELETE FROM pixie_messages")

    # 1. Create Business Owner
    owner_pw = generate_password_hash("owner123")
    cursor.execute('''
    INSERT INTO users (name, email, password_hash, role, phone, interests, avatar)
    VALUES (?, ?, ?, 'owner', ?, ?, ?)
    ''', ("Sarah Jenkins (Founder)", "owner@marketmind.ai", owner_pw, "+91 98765 43210", "Business Strategy, Brand Growth, Growth Hacking", "👩‍💼"))
    owner_id = cursor.lastrowid

    # 2. Create Business Profile with Full Contact Info
    cursor.execute('''
    INSERT INTO business_profiles (user_id, business_name, industry, target_audience, location, budget, products_services, contact_phone, contact_email, contact_whatsapp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        owner_id,
        "Aura Trends Fashion Co.",
        "Fashion & College Streetwear",
        "College students aged 18–24, youth creators, college fest attendees",
        "Bangalore & New Delhi, India",
        80000.0,
        "Oversized Graphic Tees, French Terry Hoodies, Campus Bags, Cargo Pants, Sticker Packs",
        "+91 98765 43210",
        "founder@auratrends.com",
        "+91 98765 43210"
    ))

    # 3. Create Part-time Employees
    emp_pw = generate_password_hash("employee123")
    employees = [
        ("Alex Rivera", "alex@marketmind.ai", emp_pw, "+91 98111 22334", "Instagram Reels, Video Editing, Gen-Z Aesthetics", "🎬"),
        ("Priya Sharma", "priya@marketmind.ai", emp_pw, "+91 98222 33445", "Meme Marketing, WhatsApp Groups, Student Clubs, Campus Outreach", "📱"),
        ("Rohit Verma", "rohit@marketmind.ai", emp_pw, "+91 98333 44556", "Campus Outreach, College Fests, Event Sponsorships, Micro-influencers", "🎨")
    ]
    emp_ids = []
    for emp in employees:
        cursor.execute('''
        INSERT INTO users (name, email, password_hash, role, phone, interests, avatar)
        VALUES (?, ?, ?, 'employee', ?, ?, ?)
        ''', emp)
        emp_ids.append(cursor.lastrowid)

    # 4. Create Active Campaigns
    campaigns = [
        (owner_id, "College Fest Sale", "Instagram", "Students aged 18–24", 10000.0, 7850.0, 7, "Active", 28400, 3210, 142, emp_ids[0]),
        (owner_id, "Freshers Welcome Bundle", "WhatsApp", "First-year College Entrants", 5000.0, 4100.0, 5, "Active", 14200, 1890, 98, emp_ids[1]),
        (owner_id, "Campus Ambassador Drop", "YouTube", "Creative youth aged 17–25", 15000.0, 11200.0, 14, "Active", 34100, 2750, 110, emp_ids[2]),
        (owner_id, "High Intent Search Campaign", "Google Ads", "Students searching college streetwear", 12000.0, 9350.0, 10, "Active", 7820, 1390, 84, None),
        (owner_id, "Fest VIP Early Access Blast", "Email", "Registered newsletter subscribers", 3000.0, 2100.0, 4, "Active", 8500, 1120, 65, None)
    ]
    camp_ids = []
    for camp in campaigns:
        cursor.execute('''
        INSERT INTO campaigns (user_id, title, channel, target_audience, budget, spent, duration_days, status, reach, clicks, conversions, assigned_employee_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', camp)
        camp_ids.append(cursor.lastrowid)

    # 5. Create Employee Tasks (Matched to interests)
    tasks = [
        (camp_ids[0], emp_ids[0], "Create 3 Viral Instagram Reels for College Fest Drop", "Shoot and edit 3 high-energy 15-second reels showcasing oversized streetwear outfits with trending audio.", "Instagram", 1500.0, "Instagram Reels, Video Editing", "In Progress", "", ""),
        (camp_ids[1], emp_ids[1], "College WhatsApp Group & Status Broadcast Blast", "Distribute student discount posters and link into 8 active college student groups with unique referral code.", "WhatsApp", 800.0, "WhatsApp Groups, Campus Outreach", "Submitted", "https://instagram.com/p/example_post", "Shared across 8 campus WhatsApp communities reaching over 1,400 students! Click tracking link generated 120 visits so far."),
        (camp_ids[0], None, "Design 2 Relatable Campus Meme Ads for Midterm Season", "Create relatable student memes highlighting comfort during long coding & lecture hours wearing Aura graphic tees.", "Instagram / Reddit", 1000.0, "Meme Marketing, Social Media", "Available", "", ""),
        (camp_ids[2], emp_ids[2], "Campus Ambassador Postcard & QR Flyer Distribution", "Distribute 60 branded discount postcards around campus food courts and cultural fest boards.", "Campus Outreach", 1200.0, "Campus Outreach, Event Sponsorships", "Approved", "https://photos.app.goo.gl/example", "Distributed all 60 cards at RV College Canteen. Feedback was super positive!")
    ]
    for task in tasks:
        cursor.execute('''
        INSERT INTO employee_tasks (campaign_id, assigned_employee_id, title, description, channel, reward_inr, tags, status, proof_url, proof_text)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', task)

    # 6. Create Customer Segments
    segments = [
        (owner_id, "New Customers", "First purchase within 30 days, exploring product variety", 1240, 850.0, "Send automated WhatsApp welcome sequence + 15% discount voucher for second order within 14 days."),
        (owner_id, "Loyal Customers", "5+ repeat purchases, high engagement and brand affinity", 480, 4200.0, "Enroll into 'Aura VIP Campus Circle' with free limited edition tote bags and early 24-hr access to new drops."),
        (owner_id, "High Value", "High basket spending (> ₹3,500 per order) across outerwear & sets", 310, 6800.0, "Offer exclusive concierge styling service, customized gift boxes, and invitations to co-design fest apparel."),
        (owner_id, "Inactive", "No purchases or app visits in the last 90 days", 890, 620.0, "Trigger 'We Miss You' retargeting email and SMS with a ₹250 instant cash voucher valid for 72 hours.")
    ]
    for seg in segments:
        cursor.execute('''
        INSERT INTO customer_segments (user_id, segment_name, characteristics, customer_count, avg_spend, ai_strategy)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', seg)

    # 7. Create Competitors Analysis
    competitors = [
        (owner_id, "UrbanCraze", "Strong Instagram presence (120k followers) and clean aesthetic feed", "Slow customer support replies and generic non-college themes", "Deploy hyper-local campus student ambassadors for authentic word-of-mouth and hostel deliveries."),
        (owner_id, "BudgetWear", "Extremely low prices (₹399 graphic tees)", "Thin 160 GSM fabric, high shrinking and fading after single wash", "Emphasize 'Affordable Luxury' with heavyweight 240 GSM combed cotton that outlasts 50+ washes."),
        (owner_id, "CampusChic", "Strong historical college reputation and positive alumni reviews", "Completely absent on Instagram Reels, TikTok, and WhatsApp automations", "Dominate short-form video content with relatable student humor and frictionless 1-click UPI checkout.")
    ]
    for comp in competitors:
        cursor.execute('''
        INSERT INTO competitor_analyses (user_id, competitor_name, key_strengths, weaknesses, differentiation_strategy)
        VALUES (?, ?, ?, ?, ?)
        ''', comp)

    # 8. Create AI Marketing Recommendation Engine items
    recommendations = [
        (owner_id, "Engagement Rate dropped by 18% this month", "Social interaction dips can lead to lower algorithmic distribution and increased acquisition cost.", "Post short-form vertical videos 3–4 times per week and target users aged 18–24 between 6 PM and 9 PM featuring student styling hauls.", "Content Timing & Format"),
        (owner_id, "Instagram Ad CPC increased by 22%", "Ad creative fatigue detected across image carousel variants.", "Rotate ad creative: replace static product photos with real student video unboxings and canteen styling challenges.", "Creative Refresh"),
        (owner_id, "64% College Mobile Cart Abandonment", "Visitors bounce when encountering traditional multi-step checkout.", "Activate 1-Click WhatsApp & UPI instant checkout with an instant ₹100 student verification credit.", "Friction Reduction")
    ]
    for rec in recommendations:
        cursor.execute('''
        INSERT INTO ai_recommendations (user_id, metric_issue, impact_text, ai_recommendation_text, action_category)
        VALUES (?, ?, ?, ?, ?)
        ''', rec)

    conn.commit()
    conn.close()
    print("[Seed Data] MarketMind database successfully populated with rich demo data!")

if __name__ == "__main__":
    seed_database()
