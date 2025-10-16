import os
from flask import Flask, request, jsonify, render_template_string, session
from dotenv import load_dotenv

# LangChain & Groq
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "super_secret_key"

# 🏪 Sample inventory
INVENTORY = [
    {"name": "Rice", "price": 60},
    {"name": "Milk", "price": 50},
    {"name": "Biscuits", "price": 40},
    {"name": "Sugar", "price": 50},
    {"name": "Cooking Oil", "price": 200},
    {"name": "Tea Pack", "price": 150},
    {"name": "Soap", "price": 30},
    {"name": "Toothpaste", "price": 80},
]

# 🧠 Groq LLM setup
chat_model = None
conversation = None

# 🧩 HTML Interface
HTML_TEMPLATE = """ 
<!DOCTYPE html>
<html>
<head>
    <title>Kirana Store + AI (LangChain)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; background: #f7f7f7; }
        h1 { color: #333; }
        table { border-collapse: collapse; margin-bottom: 10px; }
        table, th, td { border: 1px solid #ccc; padding: 8px; }
        th { background: #eee; }
        input[type=number] { width: 60px; padding: 5px; }
        button { padding: 10px 15px; border: none; background: #007BFF; color: white; cursor: pointer; border-radius: 5px; }
        button:hover { background: #0056b3; }
        .chat-container { max-width: 600px; margin-top: 20px; }
        .message { padding: 10px; margin: 5px 0; border-radius: 8px; }
        .user { background: #007BFF; color: white; text-align: right; }
        .ai { background: #28a745; color: white; text-align: left; }
        #loader { display: none; }
    </style>
</head>
<body>
<h1>🛒 Kirana Store + 💬 AI Assistant (LangChain + Groq)</h1>

{% if not api_key %}
<form id="keyForm">
    <label><b>Enter Groq API Key:</b></label><br>
    <input type="password" id="apiKey" placeholder="gsk_********" required>
    <button type="submit">Save Key</button>
</form>
<p id="keyError" style="color:red;"></p>
{% else %}
<table>
    <tr><th>Item</th><th>Price (₹)</th><th>Quantity</th></tr>
    {% for item in inventory %}
    <tr>
        <td>{{item.name}}</td>
        <td>{{item.price}}</td>
        <td><input type="number" class="qty" data-price="{{item.price}}" data-name="{{item.name}}" value="0" min="0"></td>
    </tr>
    {% endfor %}
</table>

<p>Total Price: ₹<span id="totalPrice">0</span></p>

<textarea id="customRequest" rows="3" cols="60" placeholder="Or type a custom request..."></textarea><br>
<button id="sendBtn">Ask AI</button>
<button id="clearBtn" style="background:#dc3545;">Clear History</button>
<div id="loader">🤖 AI is typing...</div>

<div class="chat-container" id="chatContainer"></div>
{% endif %}

<script>
{% if api_key %}
const qtyInputs = document.querySelectorAll('.qty');
const totalPriceElem = document.getElementById('totalPrice');
const chatContainer = document.getElementById('chatContainer');

function updateTotal() {
    let total = 0;
    qtyInputs.forEach(input => {
        total += parseInt(input.value) * parseInt(input.dataset.price);
    });
    totalPriceElem.innerText = total;
}
qtyInputs.forEach(input => input.addEventListener('input', updateTotal));

document.getElementById('sendBtn').addEventListener('click', async () => {
    const loader = document.getElementById('loader');
    loader.style.display = 'block';

    let order = [];
    qtyInputs.forEach(input => {
        if(parseInt(input.value) > 0) {
            order.push(input.value + " x " + input.dataset.name + " (₹" + input.value*input.dataset.price + ")");
        }
    });

    let custom = document.getElementById('customRequest').value.trim();
    let question = custom ? custom : order.join(", ");
    if(!question) { alert("Select items or type a request!"); loader.style.display='none'; return; }

    const userDiv = document.createElement('div');
    userDiv.className = 'message user';
    userDiv.innerText = question;
    chatContainer.appendChild(userDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    const response = await fetch('/ajax_chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question})
    });
    const data = await response.json();
    loader.style.display = 'none';

    const aiDiv = document.createElement('div');
    aiDiv.className = 'message ai';
    aiDiv.innerText = data.response;
    chatContainer.appendChild(aiDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
});

document.getElementById('clearBtn').addEventListener('click', async () => {
    const res = await fetch('/clear_history', {method:'POST'});
    const data = await res.json();
    if(data.success){
        chatContainer.innerHTML = "";
        alert("History cleared!");
    }
});
{% else %}
document.getElementById('keyForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const key = document.getElementById('apiKey').value.trim();
    const res = await fetch('/set_key_ajax', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({api_key: key})
    });
    const data = await res.json();
    if(data.success) location.reload();
    else document.getElementById('keyError').innerText = data.error;
});
{% endif %}
</script>
</body>
</html>
"""

# 🧠 Initialize Groq model with LangChain
def init_groq(key):
    """Initialize Groq model with LangChain ConversationChain."""
    global chat_model, conversation
    chat_model = ChatGroq(
        api_key=key,
        model_name="llama-3.3-70b-versatile"
    )

    template = """You are a smart Kirana store assistant.
Below is the conversation history and the latest user question.
Use the history to maintain context.

Conversation History:
{history}

User Query:
{input}

If order details are given, calculate total and provide summary.
Inventory reference:
Rice ₹60/kg, Milk ₹50/ltr, Biscuits ₹40, Sugar ₹50 (500g),
Cooking Oil ₹200, Tea Pack ₹150, Soap ₹30, Toothpaste ₹80.
"""

    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=template
    )

    memory = ConversationBufferMemory(
        memory_key="history",
        input_key="input",
        return_messages=False
    )

    conversation = ConversationChain(
        llm=chat_model,
        memory=memory,
        prompt=prompt,
        verbose=False
    )

# 🏠 Home page
@app.route("/", methods=["GET"])
def home():
    api_key = session.get("api_key")
    return render_template_string(HTML_TEMPLATE, api_key=bool(api_key), inventory=INVENTORY)

# 🔑 Set API key
@app.route("/set_key_ajax", methods=["POST"])
def set_key_ajax():
    data = request.get_json()
    api_key = data.get("api_key", "").strip()
    try:
        init_groq(api_key)
        session["api_key"] = api_key
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# 💬 AJAX chat endpoint
@app.route("/ajax_chat", methods=["POST"])
def ajax_chat():
    global conversation
    if not conversation:
        api_key = session.get("api_key")
        if not api_key:
            return jsonify({"response": "❌ API key not set"})
        init_groq(api_key)

    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"response": "⚠️ Please provide a valid request!"})

    try:
        result = conversation.run(input=question)
        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"response": f"⚠️ Groq Error: {str(e)}"})

# 🧹 Clear chat memory
@app.route("/clear_history", methods=["POST"])
def clear_history():
    api_key = session.get("api_key")
    if api_key:
        init_groq(api_key)
    return jsonify({"success": True})

# 🚀 Run app
if __name__ == "__main__":
    app.run(debug=True)
