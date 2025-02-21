from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow React frontend to communicate with Flask backend

# Sample FAQ database
faqs = {
    "What services do you offer?": "We provide web and system development for businesses and companies.",
    "How much do your services cost?": "Our pricing depends on project scope. Contact us for a free quote. You will find our contact details on the contact Page and Footer",
    "How long does it take to develop a website?": "A typical website takes 2-6 weeks, depending on complexity.",
}

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.json
    user_message = data.get("message", "").strip()

    # Check if message matches an FAQ
    response = faqs.get(user_message, "I'm not sure. Would you like to schedule a consultation?")
    
    return jsonify({"response": response})

@app.route("/store_lead", methods=["POST"])
def store_lead():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")
    
    # Here, you would save data to a database
    print(f"New Lead: {name}, {email}, {message}")
    
    return jsonify({"message": "Lead saved successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
