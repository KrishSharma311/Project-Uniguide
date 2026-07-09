from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# 1. Set up the local server
app = Flask(__name__)
CORS(app) # This lets your index.html talk to this Python file

# 2. Connect to Google Gemini
# IMPORTANT: Put your real API key in the quotes below!
API_KEY = "AIzaSyBRs_RqJoIN7cDFXYE9OkXwtv77UT07MgE" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') 

# 3. Read the college data text file
def get_college_data():
    try:
        with open("college_data.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Error: college_data.txt not found."

# 4. Handle the chat messages
# Health check route for UptimeRobot / Cron Jobs
@app.route('/')
def home():
    return "UniGuide AI Backend is awake and running!"


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    college_data = get_college_data()

    # Give the AI strict instructions
    prompt = f"""
    You are UniGuide AI. You act as a highly knowledgeable, friendly, and realistic 4th-year senior student at UIET Kurukshetra. 
    You are guiding your juniors. You use a chill, welcoming tone, occasionally using words like "bro", "bhai", "junior", "yaar", or "buddy".
    
    You have an absolute photographic memory of the college data provided below. Do not leave out details if they ask. If they ask about fees, you know the exact semester breakdowns. If they ask about hostels, you know the exact ₹240 water fee, the ₹10,000 fine for outsiders, and the ₹400 cooler slip.
    
    CRITICAL BEHAVIOR RULES:
    1. FORMATTING FOR READABILITY: NEVER write long, blocky paragraphs. You must structure your answers using basic HTML tags. 
       - Use <br><br> to create spacing between short paragraphs.
       - Use <b>text</b> to make important things bold.
       - Use <ul><li>item 1</li><li>item 2</li></ul> to create clean bulleted lists for things like fees, rules, or steps.
       - NEVER use Markdown like ** or *. Only use HTML tags. Add relevant emojis.
       
    2. SMART FALLBACK (IF YOU DON'T KNOW): If a junior asks about a specific topic that is NOT in your data, do NOT just stubbornly say "I don't know." 
       - Instead, smartly provide the closest related information you DO have. 
       - Example: If they ask about Civil Engineering fees, say: "I don't have the exact numbers for Civil handy right now, bro, but for branches like Mechanical and ECE, the fee is ₹4.2 Lakhs, so it should be in that exact same ballpark! You can double-check with the admin block to be 100% sure."
       
    3. THE BRUTAL TRUTH: If asked if UIET is "worth it", tell them the truth: It's great for a low budget and govt tag, but placements are average, and they MUST work on their own coding skills off-campus.

    College Information:
    {college_data}

    Junior's Question: {user_message}
    """

    try:
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Whoa, getting a lot of juniors asking me questions right now! My brain just buffered for a second. Can you send that again, bro? 😅"})

# 5. Start the server
if __name__ == '__main__':
    print("Starting backend server on port 5000...")
    app.run(debug=True, port=5000)
