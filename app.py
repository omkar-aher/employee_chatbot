from flask import Flask, render_template, request, jsonify
from chat_agent import EmployeeChatAgent

app = Flask(__name__)
chat_agent = EmployeeChatAgent()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    question = request.json.get('question', '')
    response = chat_agent.get_response(question)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True) 