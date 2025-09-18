# 🛒 Kirana Store + 💬 AI Assistant

A modern interactive Kirana (grocery) store assistant built with **Flask**, **Groq AI**, and **AJAX**.  
Users can select grocery items with quantities, ask custom requests, and receive AI-generated responses in real-time. Features include **chat bubbles, real-time total price calculation, and clear chat history**.

---

## **Features**

- ✅ Select multiple items with quantities from inventory
- ✅ Real-time total price calculation
- ✅ Custom requests supported
- ✅ Interactive chat with AI using **Groq API**
- ✅ Chat bubbles for better user experience
- ✅ Loading spinner while AI responds
- ✅ Clear chat history button
- ✅ AJAX-based communication – no page reload

---

## **Demo**

**User flow:**

1. Enter your **Groq API Key**.  
2. Select items from inventory or type a custom request.  
3. Click **Ask AI** to get a response in chat bubbles.  
4. Click **Clear History** to reset the chat.  

---

## **Technology Stack**

- **Backend:** Python, Flask  
- **AI:** Groq API (LLaMA-3.3-70b-versatile model)  
- **Frontend:** HTML, CSS, JavaScript, AJAX  
- **Data Storage:** In-memory chat history (can be extended to SQLite for persistence)  

---

## **Installation**

1. **Clone the repository**

```bash
git clone https://github.com/your-username/kirana-store-ai.git
cd kirana-store-ai
Create a virtual environment

bash
Copy code
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Install dependencies

bash
Copy code
pip install flask groq
Usage
Run the Flask app

bash
Copy code
python app.py
Open your browser and navigate to:

cpp
Copy code
http://127.0.0.1:5000/
Enter your Groq API Key.

Select items or type a custom request and click Ask AI.

Chat responses appear in chat bubbles.

Click Clear History to reset chat.

Folder Structure
bash
Copy code
├── app.py              # Main Flask application
├── README.md           # This README file
└── requirements.txt    # Python dependencies (optional)
Future Improvements
Persistent chat history using SQLite or database

Inventory stock tracking and admin panel

Order summary with total cost and optional PDF/email export

Multi-user support with login system

Autocomplete and search for large inventory

License
This project is licensed under the MIT License.

Author
Your Name – GitHub | LinkedIn

yaml
Copy code

---

If you want, I can also create a **`requirements.txt`** file and include instructions to run **with virtual environment + all dependencies**, which will make it fully ready for GitHub.  

Do you want me to do that next?






You said:
write in one


ChatGPT said:
Sure! Here’s a single, complete README.md file for your project:

markdown
Copy code
# 🛒 Kirana Store + 💬 AI Assistant

A modern interactive Kirana (grocery) store assistant built with **Flask**, **Groq AI**, and **AJAX**.  
Users can select grocery items with quantities, ask custom requests, and receive AI-generated responses in real-time. Features include **chat bubbles, real-time total price calculation, and clear chat history**.

---

## Features

- ✅ Select multiple items with quantities from inventory  
- ✅ Real-time total price calculation  
- ✅ Custom requests supported  
- ✅ Interactive chat with AI using **Groq API**  
- ✅ Chat bubbles for better user experience  
- ✅ Loading spinner while AI responds  
- ✅ Clear chat history button  
- ✅ AJAX-based communication – no page reload  

---

## Demo

**User Flow:**

1. Enter your **Groq API Key**.  
2. Select items from inventory or type a custom request.  
3. Click **Ask AI** to get a response in chat bubbles.  
4. Click **Clear History** to reset the chat.  

---

## Technology Stack

- **Backend:** Python, Flask  
- **AI:** Groq API (LLaMA-3.3-70b-versatile model)  
- **Frontend:** HTML, CSS, JavaScript, AJAX  
- **Data Storage:** In-memory chat history (can be extended to SQLite for persistence)  

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/kirana-store-ai.git
cd kirana-store-ai
Create a virtual environment

bash
Copy code
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Install dependencies

bash
Copy code
pip install flask groq
Usage
Run the Flask app

bash
Copy code
python app.py
Open your browser:

cpp
Copy code
http://127.0.0.1:5000/
Enter your Groq API Key.

Select items or type a custom request and click Ask AI.

Chat responses appear in chat bubbles.

Click Clear History to reset chat.

Folder Structure
bash
Copy code
├── app.py              # Main Flask application
├── README.md           # This README file
└── requirements.txt    # Python dependencies (optional)
Future Improvements
Persistent chat history using SQLite or database

Inventory stock tracking and admin panel

Order summary with total cost and optional PDF/email export

Multi-user support with login system

Autocomplete and search for large inventory

License
This project is licensed under the MIT License.
