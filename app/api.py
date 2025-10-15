# Add 'render_template' to your imports
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from . import database as db
from . import llm_logic

db.init_db()

# The __name__ tells Flask where to look for the templates and static folders
app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

# Add this new route to serve the webpage
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start_session():
    session_id = db.create_new_session()
    return jsonify({"session_id": session_id})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id')
    user_message = data.get('message')

    if not session_id or not user_message:
        return jsonify({"error": "session_id and message are required"}), 400

    db.add_message_to_session(session_id, 'user', user_message)
    history = db.get_session_history(session_id)
    bot_response, status = llm_logic.get_bot_response(user_message, history)

    if status == "escalate":
        summary = llm_logic.summarize_conversation(history)
        bot_response += f"\n\n**Conversation Summary for Agent:**\n{summary}"

    db.add_message_to_session(session_id, 'bot', bot_response)
    return jsonify({"response": bot_response})