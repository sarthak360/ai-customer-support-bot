import json
import requests

with open('faqs.json', 'r') as f:
    faqs = json.load(f)

OLLAMA_API_URL = "http://localhost:11434/api/chat"

# --- NEW: Define a set of common "stop words" to ignore ---
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "being", "been",
    "have", "has", "had", "do", "does", "did", "what", "which", "who",
    "whom", "this", "that", "these", "those", "am", "i", "me", "my",
    "myself", "we", "our", "ours", "you", "your", "yours", "he", "him",
    "his", "she", "her", "it", "its", "they", "them", "their", "how",
    "can", "what", "is", "your", "in", "on", "at", "for", "to", "of"
}

def find_relevant_faq(user_query):
    """
    An improved search function that ignores common stop words.
    """
    user_query = user_query.lower()
    best_match = None
    highest_score = 0

    # --- UPDATED LOGIC ---
    query_words = set(user_query.split())

    for faq in faqs:
        score = 0
        question_words = set(faq['question'].lower().split())

        # Find the important words that are in both the query and the FAQ question
        matching_keywords = query_words.intersection(question_words)

        # Calculate score based only on non-stop-words
        for word in matching_keywords:
            if word not in STOP_WORDS:
                score += 1

        if score > highest_score:
            highest_score = score
            best_match = faq

    return best_match if highest_score > 0 else None


def get_bot_response(user_message, history):
    escalation_keywords = ["human", "agent", "speak to a person", "live support"]
    if any(keyword in user_message.lower() for keyword in escalation_keywords):
        return "I understand you'd like to speak with a human agent. I am escalating your request.", "escalate"

    relevant_faq = find_relevant_faq(user_message)

    if not relevant_faq:
        return "I'm sorry, I couldn't find information related to your question in my knowledge base. Would you like to speak to a human agent?", "no_faq"

    system_prompt = f"""
    You are a friendly and helpful customer support bot.
    Your goal is to answer the user's question based *only* on the provided context.
    Do not make up information. If the context does not contain the answer, say so.
    Context: "{relevant_faq['answer']}"
    """

    messages = [{"role": "system", "content": system_prompt}]
    for message in history:
        role = "assistant" if message['role'] == 'model' else message['role']
        messages.append({"role": role, "content": message['parts'][0]})
    messages.append({"role": "user", "content": user_message})

    try:
        payload = {"model": "llama3:8b", "messages": messages, "stream": False}
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        bot_response = response.json()['message']['content']
        return bot_response, "success"
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return "Sorry, I'm having trouble connecting to my local AI model. Is Ollama running?", "error"

def summarize_conversation(history):
    history_text = "\n".join([f"{msg['role']}: {msg['parts'][0]}" for msg in history])
    summary_prompt = f"Please summarize the following customer support conversation concisely:\n\n{history_text}"
    messages = [{"role": "user", "content": summary_prompt}]
    try:
        payload = {"model": "llama3:8b", "messages": messages, "stream": False}
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        return response.json()['message']['content']
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Could not summarize the conversation."