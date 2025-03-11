# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from qa_system import EnhancedCryptoQA

# Create the Flask app
app = Flask(__name__)
CORS(app)

# Initialize QA system
qa_system = EnhancedCryptoQA()

# Serve the frontend
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint
@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question', '')
    answers = qa_system.get_answers(question)
    insights = qa_system.generate_insights(answers)
    return jsonify({
        "answers": answers,
        "insights": insights
    })

if __name__ == '__main__':
    app.run(debug=True)
