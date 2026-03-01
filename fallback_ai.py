# Fallback AI response function - works without external API
def get_fallback_response(question, language="en"):
    """Generate smart responses for general questions when AI API is not available"""
    import random
    from datetime import datetime
    
    # Convert to lowercase for matching
    q = question.lower()
    
    # General topic patterns and responses
    topic_responses = {
        'greeting': {
            'keywords': ['hello', 'hi', 'hey', 'greetings', 'namaste', 'hola', 'good morning', 'good evening'],
            'response': "Hello! I'm your Smart City AI Assistant. I can help you with recycling tips, waste management, city services, and much more! What would you like to know?"
        },
        'who_are_you': {
            'keywords': ['who are you', 'what are you', 'your name', 'about you', 'what is your name'],
            'response': "I'm your Smart City AI Assistant! I'm here to help you with any questions about recycling, waste management, city services, and general knowledge. I can answer questions on science, math, history, technology, health, cooking, travel, and more!"
        },
        'help': {
            'keywords': ['help', 'what can you do', 'capabilities', 'what can i ask', 'help me'],
            'response': "I can help you with: Recycling and waste management tips, Reporting issues to authorities, Scheduling pickups, General knowledge and education, Health and wellness advice, Cooking and recipes, Travel information, Science and math, and much more! Just ask me anything!"
        },
        'recycling': {
            'keywords': ['recycl', 'waste', 'trash', 'bin', 'compost', 'green', 'disposal', 'garbage'],
            'response': "Great question about recycling! Here are some tips: Plastics - Look for recycling numbers #1 and #2. Rinse and keep caps on. Paper - Keep dry, flatten cardboard, remove tape. Glass - Rinse, remove caps, sort by color if needed. Metal - Rinse and crush cans to save space. Organic - Compost food scraps in green bins. E-waste - Never throw electronics - take to e-waste centers! Need more specific help? Just ask!"
        },
        'plastic': {
            'keywords': ['plastic', 'bottle', 'container', 'bag'],
            'response': "Plastic recycling tips: Check for recycling numbers #1 (PET) and #2 (HDPE) - these are most commonly recycled. Rinse containers before recycling. Keep caps on bottles. Avoid plastic bags in regular recycling - take them to grocery store drop-off points. Look for the recycling bin color in your area (usually blue)."
        },
        'paper': {
            'keywords': ['paper', 'cardboard', 'newspaper', 'magazine'],
            'response': "Paper recycling tips: Keep paper dry and free from food stains. Flatten cardboard boxes to save space. Remove tape and stickers from cardboard. Shred confidential documents before recycling. Newspaper and magazines go in the paper recycling bin. Paper should be clean and dry!"
        },
        'glass': {
            'keywords': ['glass', 'bottle', 'jar'],
            'response': "Glass recycling tips: Rinse glass bottles and jars thoroughly. Remove lids and caps (recycle those separately). Some areas require sorting by color (clear, brown, green). Do not include broken glass - it is dangerous for workers. Glass is 100 percent recyclable and can be recycled infinitely!"
        },
        'metal': {
            'keywords': ['metal', 'can', 'aluminum', 'tin', 'steel'],
            'response': "Metal recycling tips: Rinse metal cans thoroughly. Crush cans to save space. Aluminum cans are 100 percent recyclable. Tin and steel cans are also recyclable. Metal recycling saves 95 percent of the energy needed to make new metal."
        },
        'ewaste': {
            'keywords': ['electronic', 'e-waste', 'battery', 'phone', 'computer', 'tv'],
            'response': "E-waste recycling: NEVER throw electronics in regular trash. Take old phones, computers, TVs to e-waste collection centers. Many electronics stores accept old devices for recycling. Batteries should be taken to special collection points. E-waste contains harmful chemicals that pollute if not disposed properly."
        },
        'compost': {
            'keywords': ['compost', 'food', 'organic', 'vegetable', 'fruit', 'garden'],
            'response': "Composting at home: Fruit and vegetable scraps, coffee grounds, tea bags, eggshells can be composted. Avoid meat, dairy, and oily foods (attract pests). Balance greens (food scraps) with browns (leaves, cardboard). Keep compost moist but not wet. Turn it regularly to speed up decomposition. In 2-6 months, you will have nutrient-rich compost for your garden!"
        },
        'weather': {
            'keywords': ['weather', 'temperature', 'rain', 'sunny', 'climate', 'forecast'],
            'response': "I don't have real-time weather data, but you can check your local weather app or website for current conditions. Would you like tips on how weather affects recycling or waste management in your area?"
        },
        'time': {
            'keywords': ['time', 'date', 'today', 'what is the time'],
            'response': "The current time is " + datetime.now().strftime('%I:%M %p') + " and today's date is " + datetime.now().strftime('%B %d, %Y') + ". Is there anything else you'd like to know?"
        },
        'thanks': {
            'keywords': ['thank', 'thanks', 'appreciate', 'thx', 'grateful'],
            'response': "You're welcome! I'm happy to help. Feel free to ask me anything else about recycling, waste management, or any other topic!"
        },
        'goodbye': {
            'keywords': ['bye', 'goodbye', 'see you', 'later', 'exit', 'take care'],
            'response': "Goodbye! It was great chatting with you. Come back anytime you have questions about recycling, city services, or anything else!"
        },
        'joke': {
            'keywords': ['joke', 'funny', 'laugh', 'humor'],
            'response': "Here's a recycling joke for you: Why did the paper go to school? Because it wanted to be recycled! Need more jokes or have another question?"
        },
        'motivation': {
            'keywords': ['motivate', 'inspire', 'quote', 'encourage'],
            'response': "Here's an inspiring quote: 'We don't need a handful of people doing zero waste perfectly. We need millions of people doing it imperfectly.' - Anne Marie Bonneau. Every small action counts! What else would you like to know?"
        },
        'smart_bin': {
            'keywords': ['smart bin', 'smart bin app', 'how does it work'],
            'response': "The Smart City Assistant app helps you: Report waste and recycling issues, Request garbage pickup, Check bin status, Get recycling tips, Report problems to ward authorities, Schedule pickups, Earn points on the leaderboard. Just explore the app to discover all features!"
        },
        'authority': {
            'keywords': ['authority', 'ward', 'complaint', 'report problem'],
            'response': "To report issues to ward authorities: Use the 'Report Issue' button in the app, Select the type of problem, Describe the issue in detail, The ward authority will be notified. You can also use the 'Alert' feature to send urgent messages to the sanitation department!"
        },
        'pickup': {
            'keywords': ['pickup', 'collect', 'garbage truck', 'when'],
            'response': "To request garbage pickup: Use the 'Request Pickup' button in the dashboard, Or schedule a specific date and time, Pickup is usually done within 2 hours of request. You can also see the bin status to check fill levels!"
        },
        'points': {
            'keywords': ['point', 'score', 'leaderboard', 'reward', 'earn'],
            'response': "Earn points on the Smart City leaderboard: Report recycling issues, Use the app regularly, Help keep your ward clean. Check the Leaderboard to see your rank and compete with other users!"
        }
    }
    
    # Check question against all topic patterns
    for topic, data in topic_responses.items():
        for keyword in data['keywords']:
            if keyword in q:
                return data['response']
    
    # Handle translation requests for non-English
    if language == "es":
        return "Entendido! No tengo acceso a la IA en este momento, pero puedo ayudarte con preguntas basicas sobre reciclaje y gestion de residuos. Que te gustaria saber? (Try asking in English for better results)"
    elif language == "fr":
        return "Je comprends ! Je n'ai pas acces a l'IA en ce moment, mais je peux vous aider avec des questions de base sur le recyclage. Qu'aimeriez-vous savoir ?"
    elif language == "hi":
        return "Main samjhta hoon! Mere paas abhi AI access nahi hai, lekin main recycling aur waste management ke basic questions mein madad kar sakta hoon. Aap kya jaanana chahenge?"
    elif language == "zh":
        return "Wo mingbai le! Woben keyi fangwen AI, danshi keyi bangzhu ji ben de huanwu guanli he huanli wenti. Nin xiang zhidao shenme?"
    
    # Default helpful response for any other question
    default_responses = [
        "That's an interesting question! I'm your Smart City Assistant. I can help you with: Recycling tips and waste management, City services information, Reporting issues, General knowledge. What would you like to explore?",
        "Great question! I specialize in helping with recycling and waste management. Try asking me about: What can I recycle? How to compost at home? E-waste disposal? Smart city features? Or ask me anything else!",
        "I'd be happy to help! As your Smart City Assistant, I can answer questions about recycling, waste disposal, city services, and more. What would you like to know?",
        "Interesting! I'm best at helping with recycling and waste management. Try questions like 'What can I recycle?' or 'How do I compost?' - or ask me about the Smart City app features!"
    ]
    
    return random.choice(default_responses)
