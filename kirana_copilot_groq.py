from flask import Flask, request, jsonify, render_template_string, session
from groq import Groq
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Sample inventory with price
INVENTORY = [
    {"name": "Rice", "price": 60},       # per kg
    {"name": "Milk", "price": 50},       # per litre
    {"name": "Biscuits", "price": 40},   # per packet
    {"name": "Sugar", "price": 50},      # per 500g
    {"name": "Cooking Oil", "price": 200},
    {"name": "Tea Pack", "price": 150},
    {"name": "Soap", "price": 30},
    {"name": "Toothpaste", "price": 80},
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Kirana Store + AI</title>
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
<h1>🛒 Kirana Store + 💬 AI Assistant</h1>

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

client = None
chat_history = []  # in-memory for AJAX demo

@app.route("/", methods=["GET"])
def home():
    api_key = session.get("api_key")
    return render_template_string(HTML_TEMPLATE, api_key=bool(api_key), inventory=INVENTORY)

@app.route("/set_key_ajax", methods=["POST"])
def set_key_ajax():
    global client
    data = request.get_json()
    api_key = data.get("api_key","").strip()
    try:
        test_client = Groq(api_key=api_key)
        test_client.models.list()  # simple validation
        session["api_key"] = api_key
        client = test_client
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": f"Invalid API Key: {str(e)}"})

@app.route("/ajax_chat", methods=["POST"])
def ajax_chat():
    global client, chat_history
    if not client:
        api_key = session.get("api_key")
        if not api_key:
            return jsonify({"response": "API key not set!"})
        client = Groq(api_key=api_key)

    data = request.get_json()
    question = data.get("question","").strip()
    if not question:
        return jsonify({"response": "Please provide a valid request!"})

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a Kirana store assistant. Include inventory and total cost info if provided."},
                {"role": "user", "content": question}
            ],
            model="llama-3.3-70b-versatile"
        )
        response_text = completion.choices[0].message.content
    except Exception as e:
        response_text = f"⚠️ Error calling Groq API: {str(e)}"

    chat_history.append((question, response_text))
    return jsonify({"response": response_text})

@app.route("/clear_history", methods=["POST"])
def clear_history():
    global chat_history
    chat_history = []
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)






