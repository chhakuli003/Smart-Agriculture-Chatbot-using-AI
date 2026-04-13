from flask import Flask, render_template, request, jsonify
import requests
from utils.predict import predict_disease

app = Flask(__name__)

# 👉 Weather API (put your API key)
API_KEY = "YOUR_API_KEY"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json["message"].lower()

    if "crop" in msg:
        reply = "Recommended crops: Cotton, Soybean, Wheat."

    elif "weather" in msg:
        city = "Nagpur"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()
        temp = data["main"]["temp"]
        reply = f"Current temperature in {city} is {temp}°C"

    elif "fertilizer" in msg:
        reply = "Use NPK fertilizer depending on soil condition."

    else:
        reply = "Sorry, I didn’t understand."

    return jsonify({"reply": reply})


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]
    result = predict_disease(file)
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)
