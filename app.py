from flask import Flask, render_template, request, jsonify 
from flask_cors import CORS
import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.3,
    )
    return response.choices[0].message["content"]

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt')
    model = data.get('model', 'gpt-3.5-turbo')
    response = get_completion(prompt, model)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
