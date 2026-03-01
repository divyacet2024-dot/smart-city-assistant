from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import os
import json
from datetime import datetime
import random
import base64
from google import genai
from fallback_ai import get_fallback_response

app = Flask(__name__)
app.secret_key = 'smartbin_secret_key_2026'

# Configure Gemini AI
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = None

if GEMINI_API_KEY:
    print("Gemini Key Loaded Successfully")
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    print("Gemini Key NOT Found")  

# Demo user data (in production, use a database)
users_db = {}
sessions_db = {}

# Authority data
authorities_db = {
    "admin@smartcity.com": {
        "name": "City Admin",
        "password": "admin",
        "role": "authority"
    }
}

# AI Recycling Tips Database
recycling_tips = {
    'plastic': "Rinse plastic containers before recycling and remove caps. Place plastics in the blue bin.",
    'paper': "Flatten cardboard boxes and keep paper dry. Remove any plastic lining.",
    'glass': "Rinse glass bottles and jars. Remove lids and sort by color if required in your area.",
    'metal': "Rinse aluminum cans and steel containers. Labels can stay on.",
    'organic': "Compost food waste in green bins. Avoid adding meat or dairy to compost.",
    'electronics': "Never throw e-waste in regular bins. Take to designated e-waste collection centers.",
    'battery': "Dispose batteries at special collection points. Never throw in regular trash.",
    'clothes': "Donate usable clothes to charity or use textile recycling bins.",
    'glass bottle': "Rinse thoroughly and remove caps. Most areas accept all colors together.",
    'plastic bottle': "Crush to save space, rinse, and keep the cap on before recycling.",
    'cardboard': "Flatten boxes and remove any tape or labels. Break down large pieces.",
    'newspaper': "Keep dry and bundle with string. Can be recycled 7 times!",
    'aluminum': "Aluminum is infinitely recyclable - rinse and crush cans.",
    'food waste': "Use green bins for compost. Add to community compost programs.",
    'hazardous': "Take to hazardous waste facilities - never pour down drains or in trash."
}

# Waste identification patterns
waste_patterns = {
    'plastic': ['bottle', 'bag', 'container', 'cup', 'straw', 'utensil', 'wrapper', 'packaging'],
    'paper': ['cardboard', 'box', 'newspaper', 'magazine', 'paper', 'envelope', 'card'],
    'glass': ['bottle', 'jar', 'glass', 'vial'],
    'metal': ['can', 'foil', 'tin', 'aerosol', 'utensil'],
    'organic': ['food', 'fruit', 'vegetable', 'coffee', 'tea', 'egg'],
    'electronics': ['phone', 'cable', 'charger', 'battery', 'device', 'computer'],
    'clothes': ['shirt', 'pants', 'jacket', 'shoe', 'textile', 'fabric']
}

def identify_waste(image_description):
    """Identify waste type from image description"""
    image_description = image_description.lower()
    
    for waste_type, keywords in waste_patterns.items():
        for keyword in keywords:
            if keyword in image_description:
                return waste_type
    
    return 'general'

def get_recycling_tip(waste_type):
    """Get recycling tip for identified waste type"""
    return recycling_tips.get(waste_type, recycling_tips.get('general', 'When in doubt, check your local recycling guidelines.'))

# Routes
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("message")

    if not user_input:
        return "Please enter a question."

    if client is None:
        return "AI is currently not available"

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_input
        )

        return response.text

    except Exception as e:
        print("Error:", e)
        return "Something went wrong"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("dashboard.html", user=sessions_db.get(session.get('user_id'), {}))

@app.route("/scanner")
def scanner():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("scanner.html", user=sessions_db.get(session.get('user_id'), {}))

@app.route("/assistant")
def assistant():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("assistant.html", user=sessions_db.get(session.get('user_id'), {}))

@app.route("/leaderboard")
def leaderboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Generate mock leaderboard data with contact info
    mock_leaderboard = leaderboard_users
    
    return render_template("leaderboard.html", user=sessions_db.get(session.get('user_id'), {}), leaderboard=mock_leaderboard)

@app.route("/authority")
def authority_dashboard():
    if 'user_id' not in session or sessions_db.get(session.get('user_id'), {}).get('role') != 'authority':
        return redirect(url_for('login'))
    return render_template("authority.html", user=sessions_db.get(session.get('user_id'), {}))

# Authentication routes
@app.route("/api/signup", methods=["POST"])
def api_signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if email in users_db:
        return jsonify({"success": False, "message": "Email already registered!"}), 400
    
    users_db[email] = {
        "name": name,
        "email": email,
        "password": password,
        "created_at": datetime.now().isoformat()
    }
    
    user_id = f"user_{len(sessions_db) + 1}"
    sessions_db[user_id] = users_db[email]
    session['user_id'] = user_id
    
    return jsonify({"success": True, "message": "Account created successfully!"})

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    login_type = data.get('type', 'email')
    
    if login_type == 'google':
        # Simulate Google OAuth - in production, use Google OAuth
        user_id = f"google_{email.replace('@', '_at_')}"
        user_data = {
            "name": email.split('@')[0].replace('.', ' ').title(),
            "email": email,
            "auth_type": "google"
        }
        sessions_db[user_id] = user_data
        session['user_id'] = user_id
        return jsonify({"success": True, "message": "Logged in with Google!"})
    
    # Email login
    if email in authorities_db and authorities_db[email]["password"] == password:
        user_id = f"auth_{email.replace('@', '_at_')}"
        sessions_db[user_id] = authorities_db[email]
        session['user_id'] = user_id
        return jsonify({"success": True, "message": "Logged in as Authority!", "redirect": "/authority"})

    if email not in users_db:
        return jsonify({"success": False, "message": "Email not registered!"}), 400
    
    if users_db[email]["password"] != password:
        return jsonify({"success": False, "message": "Incorrect password!"}), 400
    
    user_id = f"user_{email.replace('@', '_at_')}"
    sessions_db[user_id] = users_db[email]
    session['user_id'] = user_id
    
    return jsonify({"success": True, "message": "Logged in successfully!", "redirect": "/dashboard"})

@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.pop('user_id', None)
    return jsonify({"success": True, "message": "Logged out successfully!"})

# Smart Scanner AI routes
@app.route("/api/scan", methods=["POST"])
def api_scan():
    data = request.json
    image_data = data.get('image', '')
    description = data.get('description', '')
    language = data.get('language', 'en')
    
    if GEMINI_API_KEY and image_data:
        try:
            # Remove data:image/jpeg;base64, prefix
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"""
            Analyze this image of waste/trash. 
            Identify the item, its category (plastic, paper, glass, metal, organic, electronics, or general), 
            whether it is recyclable (true/false), and provide a 1-sentence personalized tip on how to recycle it correctly.
            Also provide 3 short step-by-step instructions.
            Respond ONLY in valid JSON format like this:
            {{
                "item": "Name of item",
                "category": "category name",
                "recyclable": true,
                "tip": "1-sentence tip",
                "instructions": "1. Step 1\\n2. Step 2\\n3. Step 3"
            }}
            Please translate the 'item', 'tip', and 'instructions' to language code: {language}.
            """
            
            response = model.generate_content([
                {'mime_type': 'image/jpeg', 'data': image_bytes},
                prompt
            ])
            
            result_text = response.text.strip()
            if result_text.startswith('```json'):
                result_text = result_text[7:-3]
            elif result_text.startswith('```'):
                result_text = result_text[3:-3]
                
            ai_data = json.loads(result_text)
            
            return jsonify({
                "success": True,
                "item": ai_data.get("item", "Unknown Item"),
                "category": ai_data.get("category", "general").lower(),
                "tip": ai_data.get("tip", "Please dispose of properly."),
                "recyclable": ai_data.get("recyclable", False),
                "instructions": ai_data.get("instructions", "1. Clean\\n2. Sort\\n3. Dispose")
            })
        except Exception as e:
            print(f"Gemini API Error: {e}")
            # Fallback to mock if API fails
            pass

    # Fallback to mock logic
    image_description = description
    waste_type = identify_waste(image_description)
    tip = get_recycling_tip(waste_type)
    item_name = image_description.title() if image_description else "Unknown Item"
    
    return jsonify({
        "success": True,
        "item": item_name,
        "category": waste_type,
        "tip": tip,
        "recyclable": waste_type in ['plastic', 'paper', 'glass', 'metal'],
        "instructions": f"1. Clean the item thoroughly\n2. Remove any labels if required\n3. Place in {waste_type} recycling bin"
    })

# AI Assistant route - GENERAL PURPOSE AI
@app.route("/api/ask", methods=["POST"])
def api_ask():
    data = request.json
    question = data.get("question", "")
    language = data.get("language", "en")

    # First try Gemini API if available
    if client:
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"""
You are a helpful AI assistant.
Respond clearly and helpfully.

Language: {language}
User Question: {question}
"""
            )

            return jsonify({
                "success": True,
                "answer": response.text,
                "timestamp": datetime.now().isoformat()
            })

        except Exception as e:
            print("Gemini API Error:", e)

    # Fallback: Use local AI system when API is not available
    answer = get_fallback_response(question, language)
    return jsonify({
        "success": True,
        "answer": answer,
        "timestamp": datetime.now().isoformat()
    })

# Existing bin functionality routes
@app.route("/sanitation")
def sanitation():
    return jsonify({
        "message": "Complaint sent to Ward 2 Sanitation Authority"
    })

@app.route("/alert")
def alert():
    return jsonify({
        "message": "Garbage pickup scheduled at 9 AM"
    })

@app.route("/api/request-pickup", methods=["POST"])
def request_pickup():
    return jsonify({
        "success": True,
        "message": "Pickup request sent! Garbage truck will arrive within 2 hours."
    })

@app.route("/api/report-issue", methods=["POST"])
def report_issue():
    data = request.json
    issue_type = data.get('issue', 'General')
    return jsonify({
        "success": True,
        "message": f"Issue reported ({issue_type})! Maintenance team will be notified."
    })

@app.route("/api/schedule-pickup", methods=["POST"])
def schedule_pickup():
    data = request.json
    date = data.get('date')
    time = data.get('time')
    return jsonify({
        "success": True,
        "message": f"Pickup scheduled for {date} at {time}"
    })

@app.route("/api/ward-alert", methods=["POST"])
def ward_alert():
    data = request.json
    message = data.get('message', 'General alert')
    return jsonify({
        "success": True,
        "message": f"Alert sent to Ward Authority: \"{message}\""
    })

# Get bin status
@app.route("/api/bin-status")
def bin_status():
    return jsonify({
        "fill_level": random.randint(40, 90),
        "battery": random.randint(60, 100),
        "temperature": random.randint(20, 35),
        "location": "Ward 12, Main Street",
        "last_collection": "2 hours ago"
    })

# ====== NEW FEATURES ======

# Eco Tips Database
eco_tips = [
    {"id": 1, "title": "Zero Waste Kitchen", "tip": "Use reusable containers instead of plastic wrap. It saves money and reduces plastic waste!", "category": "lifestyle", "points": 10},
    {"id": 2, "title": "Compost Food Scraps", "tip": "Did you know 30% of household waste is food? Composting reduces methane and creates free fertilizer!", "category": "composting", "points": 15},
    {"id": 3, "title": "E-Waste Awareness", "tip": "One phone contains toxic materials. Always recycle electronics at certified e-waste centers.", "category": "electronics", "points": 20},
    {"id": 4, "title": "Plastic Free July", "tip": "Bring your own bags, bottles, and containers. Avoid single-use plastics whenever possible!", "category": "lifestyle", "points": 10},
    {"id": 5, "title": "Paper Recycling", "tip": "Paper can be recycled up to 7 times! Always flatten boxes and remove tape before recycling.", "category": "recycling", "points": 10},
    {"id": 6, "title": "Glass Recycling", "tip": "Glass is 100% recyclable and can be recycled endlessly without losing quality!", "category": "recycling", "points": 10},
    {"id": 7, "title": "Clothing Recycling", "tip": "Only 15% of clothes are recycled. Donate usable items or use textile recycling bins.", "category": "recycling", "points": 15},
    {"id": 8, "title": "Battery Disposal", "tip": "One battery can pollute 60,000 liters of water. Use proper battery recycling points!", "category": "hazardous", "points": 20},
    {"id": 9, "title": "Buy Recycled Products", "tip": "Look for products made from recycled materials to close the recycling loop!", "category": "lifestyle", "points": 10},
    {"id": 10, "title": "Community Cleanups", "tip": "Joining local cleanup events multiplies your impact. Check community boards for events!", "category": "community", "points": 25}
]

# Collection Schedule Database
collection_schedule = [
    {"day": "Monday", "types": ["General Waste", "Recycling"], "time": "8:00 AM - 12:00 PM", "wards": ["Ward 1", "Ward 2", "Ward 3"]},
    {"day": "Tuesday", "types": ["Organic/Compost", "Glass"], "time": "8:00 AM - 12:00 PM", "wards": ["Ward 4", "Ward 5"]},
    {"day": "Wednesday", "types": ["General Waste"], "time": "8:00 AM - 12:00 PM", "wards": ["Ward 6", "Ward 7", "Ward 8"]},
    {"day": "Thursday", "types": ["Recycling", "E-Waste"], "time": "8:00 AM - 12:00 PM", "wards": ["Ward 9", "Ward 10"]},
    {"day": "Friday", "types": ["General Waste", "Organic"], "time": "8:00 AM - 12:00 PM", "wards": ["Ward 11", "Ward 12"]},
    {"day": "Saturday", "types": ["Special Collection"], "time": "9:00 AM - 3:00 PM", "wards": ["All Wards"]},
    {"day": "Sunday", "types": ["Hazardous Waste"], "time": "10:00 AM - 2:00 PM", "wards": ["Designated Centers Only"]}
]

# Bin Locations Database
bin_locations = [
    {"id": 1, "name": "Central Park Bin", "type": "recycling", "lat": 40.7829, "lng": -73.9654, "address": "Central Park, North Entrance"},
    {"id": 2, "name": "Main Street Hub", "type": "general", "lat": 40.7580, "lng": -73.9855, "address": "123 Main Street"},
    {"id": 3, "name": "City Library", "type": "glass", "lat": 40.7532, "lng": -73.9822, "address": "456 Library Ave"},
    {"id": 4, "name": "Market Square", "type": "organic", "lat": 40.7614, "lng": -73.9776, "address": "789 Market Street"},
    {"id": 5, "name": "Tech Hub Plaza", "type": "e-waste", "lat": 40.7484, "lng": -73.9857, "address": "321 Tech Boulevard"},
    {"id": 6, "name": "Community Center", "type": "recycling", "lat": 40.7549, "lng": -73.9840, "address": "555 Community Drive"},
    {"id": 7, "name": "Sports Complex", "type": "general", "lat": 40.7505, "lng": -73.9934, "address": "777 Sports Way"},
    {"id": 8, "name": "Medical District", "type": "hazardous", "lat": 40.7614, "lng": -73.9700, "address": "999 Health Center Rd"}
]

# Achievements Database
achievements = [
    {"id": 1, "name": "First Recycle", "description": "Complete your first waste scan", "icon": "fa-seedling", "points": 50, "unlocked": False},
    {"id": 2, "name": "Eco Warrior", "description": "Recycle 10 items", "icon": "fa-medal", "points": 100, "unlocked": False},
    {"id": 3, "name": "Green Champion", "description": "Recycle 50 items", "icon": "fa-trophy", "points": 250, "unlocked": False},
    {"id": 4, "name": "Waste Wizard", "description": "Use all scanner features", "icon": "fa-hat-wizard", "points": 150, "unlocked": False},
    {"id": 5, "name": "Community Hero", "description": "Report 5 issues", "icon": "fa-users", "points": 200, "unlocked": False},
    {"id": 6, "name": "Week Streak", "description": "Use app for 7 days in a row", "icon": "fa-fire", "points": 100, "unlocked": False},
    {"id": 7, "name": "Carbon Saver", "description": "Save 10kg of CO2 emissions", "icon": "fa-cloud", "points": 300, "unlocked": False},
    {"id": 8, "name": "Bin Master", "description": "Find 10 recycling bins", "icon": "fa-map-marker-alt", "points": 150, "unlocked": False}
]

# User stats storage
user_stats = {}

# ====== UTILITY SERVICES (Electricity & Water) ======

# Electricity outage schedule
electricity_schedule = [
    {"date": "2026-02-26", "area": "Ward 1", "from_time": "09:00", "to_time": "12:00", "reason": "Maintenance"},
    {"date": "2026-02-26", "area": "Ward 3", "from_time": "14:00", "to_time": "17:00", "reason": "Line Repair"},
    {"date": "2026-02-27", "area": "Ward 2", "from_time": "10:00", "to_time": "13:00", "reason": "Transformer Maintenance"},
    {"date": "2026-02-27", "area": "Ward 5", "from_time": "09:00", "to_time": "11:00", "reason": "Maintenance"},
    {"date": "2026-02-28", "area": "Ward 4", "from_time": "15:00", "to_time": "18:00", "reason": "Cable Replacement"},
]

# Water supply schedule
water_schedule = [
    {"date": "2026-02-26", "area": "Ward 1", "from_time": "06:00", "to_time": "08:00", "status": "Regular Supply"},
    {"date": "2026-02-26", "area": "Ward 2", "from_time": "05:00", "to_time": "07:00", "status": "Regular Supply"},
    {"date": "2026-02-27", "area": "Ward 3", "from_time": "06:30", "to_time": "08:30", "status": "Regular Supply"},
    {"date": "2026-02-27", "area": "Ward 4", "from_time": "05:00", "to_time": "07:00", "status": "Low Pressure"},
    {"date": "2026-02-28", "area": "Ward 5", "from_time": "06:00", "to_time": "09:00", "status": "Tank Cleaning - No Supply"},
]

# Utility problem reports
utility_reports = []

# Notifications/Messages for all users
notifications = [
    {"id": 1, "type": "electricity", "title": "Scheduled Power Cut", "message": "Ward 1: Power outage on Feb 26 from 9 AM to 12 PM for maintenance", "date": "2026-02-26", "priority": "high"},
    {"id": 2, "type": "water", "title": "Water Supply Update", "message": "Ward 5: No water supply on Feb 28 from 6 AM to 9 AM for tank cleaning", "date": "2026-02-26", "priority": "medium"},
    {"id": 3, "type": "general", "title": "Weekly Schedule", "message": "Check daily electricity and water schedules below", "date": "2026-02-26", "priority": "low"},
]

# Leaderboard users with contact info
leaderboard_users = [
    {"rank": 1, "name": "Eco Warrior", "email": "warrior@eco.com", "phone": "+1234567890", "points": 2500, "items": 156, "badges": 8},
    {"rank": 2, "name": "Green Champion", "email": "champion@green.com", "phone": "+1234567891", "points": 2200, "items": 142, "badges": 7},
    {"rank": 3, "name": "Recycling Pro", "email": "pro@recycle.com", "phone": "+1234567892", "points": 1950, "items": 128, "badges": 6},
    {"rank": 4, "name": "Clean City Hero", "email": "hero@clean.com", "phone": "+1234567893", "points": 1800, "items": 115, "badges": 5},
    {"rank": 5, "name": "Waste Manager", "email": "manager@waste.com", "phone": "+1234567894", "points": 1650, "items": 102, "badges": 5},
    {"rank": 6, "name": "Eco Friendly", "email": "friendly@eco.com", "phone": "+1234567895", "points": 1500, "items": 95, "badges": 4},
    {"rank": 7, "name": "Nature Lover", "email": "lover@nature.com", "phone": "+1234567896", "points": 1350, "items": 88, "badges": 4},
    {"rank": 8, "name": "Bin Master", "email": "master@bin.com", "phone": "+1234567897", "points": 1200, "items": 75, "badges": 3},
    {"rank": 9, "name": "Smart Recycler", "email": "smart@recycle.com", "phone": "+1234567898", "points": 1050, "items": 68, "badges": 3},
    {"rank": 10, "name": "Community Star", "email": "star@community.com", "phone": "+1234567899", "points": 900, "items": 55, "badges": 2}
]

# API Routes for new features

@app.route("/api/eco-tips")
def api_eco_tips():
    return jsonify(eco_tips)

@app.route("/api/collection-schedule")
def api_collection_schedule():
    return jsonify(collection_schedule)

@app.route("/api/bin-locations")
def api_bin_locations():
    return jsonify(bin_locations)

@app.route("/api/achievements")
def api_achievements():
    return jsonify(achievements)

@app.route("/api/user-stats", methods=["GET", "POST"])
def api_user_stats():
    user_id = session.get('user_id')
    
    if request.method == "POST":
        data = request.json
        action = data.get('action')
        
        if user_id not in user_stats:
            user_stats[user_id] = {
                "points": 0,
                "items_scanned": 0,
                "issues_reported": 0,
                "bins_found": 0,
                "streak": 0,
                "last_active": None,
                "achievements": []
            }
        
        stats = user_stats[user_id]
        
        if action == "scan":
            stats["items_scanned"] += 1
            stats["points"] += 10
        elif action == "report":
            stats["issues_reported"] += 1
            stats["points"] += 15
        elif action == "find_bin":
            stats["bins_found"] += 1
            stats["points"] += 5
        elif action == "daily_login":
            today = datetime.now().date().isoformat()
            if stats.get("last_active") != today:
                stats["streak"] += 1
                stats["points"] += 20
                stats["last_active"] = today
        
        return jsonify({"success": True, "stats": stats})
    
    # GET request
    if user_id in user_stats:
        return jsonify(user_stats[user_id])
    else:
        return jsonify({
            "points": 0,
            "items_scanned": 0,
            "issues_reported": 0,
            "bins_found": 0,
            "streak": 0
        })

# Utility Routes
@app.route("/api/electricity-schedule")
def api_electricity_schedule():
    return jsonify(electricity_schedule)

@app.route("/api/water-schedule")
def api_water_schedule():
    return jsonify(water_schedule)

@app.route("/api/notifications")
def api_notifications():
    return jsonify(notifications)

@app.route("/api/report-utility", methods=["POST"])
def api_report_utility():
    data = request.json
    report_type = data.get('type')
    description = data.get('description')
    location = data.get('location')
    
    utility_reports.append({
        "id": len(utility_reports) + 1,
        "type": report_type,
        "description": description,
        "location": location,
        "status": "pending",
        "timestamp": datetime.now().isoformat()
    })
    
    return jsonify({
        "success": True,
        "message": f"{report_type.capitalize()} issue reported successfully!"
    })

@app.route("/api/leaderboard")
def api_leaderboard():
    return jsonify(leaderboard_users)

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
