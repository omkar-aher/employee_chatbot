from flask import Flask, render_template, request, jsonify
from chat_agent import EmployeeChatAgent
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time

app = Flask(__name__)
chat_agent = EmployeeChatAgent()
executor = ThreadPoolExecutor(max_workers=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        question = request.json.get('question', '')
        if not question:
            return jsonify({'response': 'Please ask a question'})
        
        # Set timeout for response
        future = executor.submit(chat_agent.get_response, question)
        try:
            response = future.result(timeout=45)  # Increased timeout
            if not response or response.startswith('Error:'):
                return jsonify({'response': 'I apologize, could you rephrase your question?'})
            return jsonify({'response': response.strip()})
        except TimeoutError:
            return jsonify({
                'response': 'I apologize for the delay. Please try a more specific question.'
            })
        except Exception as e:
            return jsonify({'response': 'I encountered an error. Please try again.'})
            
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True) 