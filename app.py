from flask import Flask, render_template, request, jsonify
from flask_ngrok import run_with_ngrok
from chatbot import get_response


app = Flask(__name__)

run_with_ngrok(app)

@app.get("/")
def index_get():
    return render_template("index.html")


@app.post("/predict")
def userchat():
    text = request.get_json().get("message")  # check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == '__main__':
    app.run()